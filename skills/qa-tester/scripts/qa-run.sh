#!/bin/bash
# qa-run.sh - Helper script for running QA tests via subagents
# Usage: ./qa-run.sh <url> [test-type] [viewport]

URL=${1:-https://spex4less.com}
TEST_TYPE=${2:-full}  # full, happy, mobile, cro, edge
VIEWPORT=${3:-390x844}  # default mobile

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧪 QA Tester Framework (Subagent Mode)${NC}"
echo "URL: $URL"
echo "Test Type: $TEST_TYPE"
echo "Viewport: $VIEWPORT"
echo ""

# Note: This script is for reference. Actual spawning is done via sessions_spawn from main session.
# Each subagent will use browser-use CLI via exec commands.

echo -e "${YELLOW}📋 To run this QA test, use the following from main session:${NC}"
echo ""

case $TEST_TYPE in
    happy|happypath)
        echo "sessions_spawn:"
        echo '  task: "QA test HAPPY PATH on '"$URL"': Use browser-use CLI via exec. Test complete purchase flow: homepage → category → product → cart → checkout → confirmation. Screenshot each step. Report bugs, errors, flow friction. Rate experience 1-10."'
        echo '  model: "openrouter/deepseek/deepseek-v3.2"'
        echo '  runTimeoutSeconds: 600'
        ;;
        
    mobile)
        echo "sessions_spawn:"
        echo '  task: "QA test MOBILE on '"$URL"': Use browser-use CLI with --screen-size '$VIEWPORT'. Test: hamburger menu, touch interactions, product swipe, mobile checkout, keyboard behavior. Screenshot each step. Report mobile-specific bugs. Rate mobile experience 1-10."'
        echo '  model: "openrouter/deepseek/deepseek-v3.2"'
        echo '  runTimeoutSeconds: 600'
        ;;
        
    cro)
        echo "sessions_spawn:"
        echo '  task: "QA test CRO AUDIT on '"$URL"': Use browser-use CLI. Check: load speeds, form friction, trust badges, hidden fees, error messages, exit opportunities. Screenshot friction points. Identify conversion killers. Return prioritized list with severity."'
        echo '  model: "openrouter/deepseek/deepseek-v3.2"'
        echo '  runTimeoutSeconds: 600'
        ;;
        
    edge|edgecases)
        echo "sessions_spawn:"
        echo '  task: "QA test EDGE CASES on '"$URL"': Use browser-use CLI. Test: empty forms, invalid inputs, out-of-stock, URL manipulation, rapid clicks, back/forward nav. Try to break it. Report crashes, errors, data loss. Return structured edge case results."'
        echo '  model: "openrouter/deepseek/deepseek-v3.2"'
        echo '  runTimeoutSeconds: 600'
        ;;
        
    full|all)
        echo "Spawn 4 parallel subagents:"
        echo ""
        echo "1. HAPPY PATH:"
        echo '   sessions_spawn:'
        echo '     task: "QA test HAPPY PATH on '"$URL"': Use browser-use CLI via exec. Test complete purchase flow. Screenshot each step. Report bugs, errors. Rate experience 1-10."'
        echo '     model: "openrouter/deepseek/deepseek-v3.2"'
        echo '     runTimeoutSeconds: 600'
        echo ""
        echo "2. MOBILE:"
        echo '   sessions_spawn:'
        echo '     task: "QA test MOBILE on '"$URL"': Use browser-use CLI with --screen-size '$VIEWPORT'. Test touch interactions, mobile checkout. Screenshot each step. Rate mobile experience 1-10."'
        echo '     model: "openrouter/deepseek/deepseek-v3.2"'
        echo '     runTimeoutSeconds: 600'
        echo ""
        echo "3. CRO AUDIT:"
        echo '   sessions_spawn:'
        echo '     task: "QA test CRO AUDIT on '"$URL"': Use browser-use CLI. Check load speeds, form friction, trust badges, hidden fees. Screenshot friction points. Return prioritized issues."'
        echo '     model: "openrouter/deepseek/deepseek-v3.2"'
        echo '     runTimeoutSeconds: 600'
        echo ""
        echo "4. EDGE CASES:"
        echo '   sessions_spawn:'
        echo '     task: "QA test EDGE CASES on '"$URL"': Use browser-use CLI. Test empty forms, invalid inputs, URL manipulation, rapid clicks. Try to break it. Report crashes/errors."'
        echo '     model: "openrouter/deepseek/deepseek-v3.2"'
        echo '     runTimeoutSeconds: 600'
        ;;
        
    *)
        echo "Unknown test type: $TEST_TYPE"
        echo "Usage: $0 <url> [happy|mobile|cro|edge|full] [viewport]"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Copy the above and run from main session${NC}"
