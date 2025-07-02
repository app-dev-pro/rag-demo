-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Fix for existing tables: Update vector dimensions from 768 to 384
-- Drop existing table and recreate with correct dimensions if it exists
-- This ensures compatibility with FastEmbed all-MiniLM-L6-v2 model (384 dimensions)
DROP TABLE IF EXISTS documents CASCADE;
DROP FUNCTION IF EXISTS match_documents(vector, int, jsonb);

-- Create a table to store your documents
create table documents (
  id uuid primary key default gen_random_uuid(),
  content text, -- corresponds to Document.pageContent
  metadata jsonb, -- corresponds to Document.metadata
  embedding vector(384) -- 384-dimensional vector for FastEmbed embeddings (all-MiniLM-L6-v2)
);

-- Create a function to search for documents
create or replace function match_documents (
  query_embedding vector(384),
  match_count int DEFAULT null,
  filter jsonb DEFAULT '{}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- Create an index to be used by the semantic search function
create index on documents 
using ivfflat (embedding vector_cosine_ops)
with (lists = 100);
