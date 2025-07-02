#!/bin/bash

echo "Setting up Supabase configuration..."
echo

if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo
    echo "Please edit .env file with your Supabase credentials:"
    echo "- SUPABASE_URL: Found in Project Settings > API"
    echo "- SUPABASE_ANON_KEY: Found in Project Settings > API"
    echo
    read -p "Press enter to continue..."
else
    echo ".env file already exists."
fi

echo
echo "Remember to:"
echo "1. Run the SQL script from supabase_setup.sql in your Supabase dashboard"
echo "2. Update the .env file with your Supabase credentials"
echo "3. Run: docker-compose build && docker-compose up -d"
echo
read -p "Press enter to continue..."
