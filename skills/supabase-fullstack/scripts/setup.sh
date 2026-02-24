#!/usr/bin/env bash
# Supabase project setup script
# Usage: bash scripts/setup.sh

set -euo pipefail

echo "🚀 Setting up Supabase..."

# Install dependencies
if command -v bun &> /dev/null; then
  PKG="bun"
elif command -v pnpm &> /dev/null; then
  PKG="pnpm"
elif command -v yarn &> /dev/null; then
  PKG="yarn"
else
  PKG="npm"
fi

echo "📦 Installing with $PKG..."
$PKG add @supabase/supabase-js @supabase/ssr
$PKG add -D supabase

# Init supabase if not already
if [ ! -d "supabase" ]; then
  echo "🔧 Initializing Supabase project..."
  npx supabase init
fi

# Create lib directory structure
mkdir -p lib/supabase

# Create .env.local if missing
if [ ! -f ".env.local" ]; then
  cat > .env.local << 'EOF'
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
EOF
  echo "📝 Created .env.local — fill in your Supabase credentials"
fi

echo "✅ Supabase setup complete!"
echo ""
echo "Next steps:"
echo "  1. Fill in .env.local with your Supabase project credentials"
echo "  2. Run: npx supabase link --project-ref <your-project-ref>"
echo "  3. Create your first migration: npx supabase migration new init"
