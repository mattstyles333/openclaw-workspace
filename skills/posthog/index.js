#!/usr/bin/env node

/**
 * PostHog Analytics Skill for OpenClaw
 * Query and analyze data from PostHog product analytics
 */

const https = require('https');
const http = require('http');
const url = require('url');

// Configuration
const CONFIG = {
    apiKey: process.env.POSTHOG_API_KEY || 'phx_13fFdUuaz2FPtMGMZ2WItgMRN1zUwrGYwRodlxG91fYpFYzZ',
    projectId: process.env.POSTHOG_PROJECT_ID || '43640',
    host: process.env.POSTHOG_HOST || 'https://eu.posthog.com'
};

// Colors
const colors = {
    red: '\x1b[0;31m',
    green: '\x1b[0;32m',
    yellow: '\x1b[1;33m',
    blue: '\x1b[0;34m',
    cyan: '\x1b[0;36m',
    nc: '\x1b[0m'
};

// API helper
function apiCall(endpoint, params = '') {
    return new Promise((resolve, reject) => {
        const apiUrl = `${CONFIG.host}/api/projects/${CONFIG.projectId}${endpoint}`;
        const fullUrl = params ? `${apiUrl}?${params}` : apiUrl;
        
        const parsedUrl = url.parse(fullUrl);
        const client = parsedUrl.protocol === 'https:' ? https : http;
        
        const options = {
            hostname: parsedUrl.hostname,
            port: parsedUrl.port,
            path: parsedUrl.path,
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${CONFIG.apiKey}`,
                'Content-Type': 'application/json'
            }
        };
        
        const req = client.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    resolve(json);
                } catch (e) {
                    resolve(data);
                }
            });
        });
        
        req.on('error', reject);
        req.end();
    });
}

// Command: events
async function queryEvents(limit = 10, after = '', eventType = '') {
    console.log(`${colors.blue}Fetching events...${colors.nc}`);
    
    const params = new URLSearchParams();
    params.append('limit', limit);
    if (after) params.append('after', after);
    if (eventType) params.append('event', eventType);
    
    try {
        const data = await apiCall('/events', params.toString());
        const results = data.results || [];
        
        console.log(`${colors.green}Found ${results.length} events${colors.nc}\n`);
        
        // Table output
        for (const event of results) {
            const time = event.timestamp ? event.timestamp.substring(0, 19) : 'N/A';
            const id = event.distinct_id ? event.distinct_id.substring(0, 20) : 'N/A';
            console.log(`${colors.cyan}Event:${colors.nc} ${event.event} | ${colors.yellow}Time:${colors.nc} ${time} | ${colors.blue}ID:${colors.nc} ${id}...`);
        }
        
        console.log(`\n${colors.blue}--- Raw JSON ---${colors.nc}`);
        console.log(JSON.stringify(data, null, 2));
        
    } catch (error) {
        console.error(`${colors.red}Error fetching events:${colors.nc}`, error.message);
    }
}

// Command: dashboards
async function listDashboards() {
    console.log(`${colors.blue}Fetching dashboards...${colors.nc}`);
    
    try {
        const data = await apiCall('/dashboards');
        const results = data.results || [];
        
        console.log(`${colors.green}Found ${results.length} dashboards${colors.nc}\n`);
        
        for (const item of results) {
            const desc = item.description ? (item.description.length > 40 ? item.description.substring(0, 40) + '...' : item.description) : 'N/A';
            console.log(`${colors.cyan}ID:${colors.nc} ${item.id} | ${colors.yellow}Name:${colors.nc} ${item.name} | ${colors.blue}Description:${colors.nc} ${desc} | ${colors.green}Created:${colors.nc} ${item.created_at.substring(0, 10)}`);
        }
        
        console.log(`\n${colors.blue}--- Raw JSON ---${colors.nc}`);
        console.log(JSON.stringify(data, null, 2));
        
    } catch (error) {
        console.error(`${colors.red}Error fetching dashboards:${colors.nc}`, error.message);
    }
}

// Command: insights
async function listInsights() {
    console.log(`${colors.blue}Fetching insights...${colors.nc}`);
    
    try {
        const data = await apiCall('/insights');
        const results = data.results || [];
        
        console.log(`${colors.green}Found ${results.length} insights${colors.nc}\n`);
        
        for (const item of results) {
            const type = item.type || 'N/A';
            console.log(`${colors.cyan}ID:${colors.nc} ${item.id} | ${colors.yellow}Name:${colors.nc} ${item.name} | ${colors.blue}Type:${colors.nc} ${type} | ${colors.green}Created:${colors.nc} ${item.created_at.substring(0, 10)}`);
        }
        
        console.log(`\n${colors.blue}--- Raw JSON ---${NC}`);
        console.log(JSON.stringify(data, null, 2));
        
    } catch (error) {
        console.error(`${colors.red}Error fetching insights:${colors.nc}`, error.message);
    }
}

// Command: funnel
async function getFunnel(funnelId) {
    if (!funnelId) {
        console.error(`${colors.red}Error: Funnel ID required${colors.nc}`);
        console.log('Usage: !posthog funnel <funnel_id>');
        return;
    }
    
    console.log(`${colors.blue}Fetching funnel ${funnelId}...${colors.nc}`);
    
    try {
        const data = await apiCall(`/insights/${funnelId}`);
        
        console.log(`${colors.green}Funnel Details:${colors.nc}\n`);
        console.log(`Name: ${data.name} | ID: ${data.id} | Type: ${data.type || 'N/A'} | Created: ${data.created_at.substring(0, 10)}`);
        
        console.log(`\n${colors.blue}--- Full JSON ---${colors.nc}`);
        console.log(JSON.stringify(data, null, 2));
        
    } catch (error) {
        console.error(`${colors.red}Error fetching funnel:${colors.nc}`, error.message);
    }
}

// Command: persons
async function queryPersons(limit = 20, search = '') {
    const params = new URLSearchParams();
    params.append('limit', limit);
    if (search) params.append('search', search);
    
    console.log(`${colors.blue}Fetching persons...${colors.nc}`);
    
    try {
        const data = await apiCall('/persons', params.toString());
        const results = data.results || [];
        
        console.log(`${colors.green}Found ${results.length} persons${colors.nc}\n`);
        
        for (const person of results) {
            const id = person.id ? person.id.substring(0, 8) : 'N/A';
            const distinctId = person.distinct_ids && person.distinct_ids[0] ? person.distinct_ids[0].substring(0, 20) : 'N/A';
            console.log(`${colors.cyan}ID:${colors.nc} ${id}... | ${colors.yellow}Distinct ID:${colors.nc} ${distinctId}... | ${colors.blue}Created:${colors.nc} ${person.created_at.substring(0, 10)}`);
        }
        
        console.log(`\n${colors.blue}--- Raw JSON ---${colors.nc}`);
        console.log(JSON.stringify(data, null, 2));
        
    } catch (error) {
        console.error(`${colors.red}Error fetching persons:${colors.nc}`, error.message);
    }
}

// Command: cohorts
async function listCohorts() {
    console.log(`${colors.blue}Fetching cohorts...${colors.nc}`);
    
    try {
        const data = await apiCall('/cohorts');
        const results = data.results || [];
        
        if (results.length === 0) {
            console.log(`${colors.yellow}No cohorts found in this project${colors.nc}`);
            return;
        }
        
        console.log(`${colors.green}Found ${results.length} cohorts${colors.nc}\n`);
        
        for (const cohort of results) {
            const count = cohort.count || 'N/A';
            console.log(`${colors.cyan}ID:${colors.nc} ${cohort.id} | ${colors.yellow}Name:${colors.nc} ${cohort.name} | ${colors.blue}Count:${colors.nc} ${count} | ${colors.green}Created:${colors.nc} ${cohort.created_at.substring(0, 10)}`);
        }
        
        console.log(`\n${colors.blue}--- Raw JSON ---${colors.nc}`);
        console.log(JSON.stringify(data, null, 2));
        
    } catch (error) {
        console.error(`${colors.red}Error fetching cohorts:${colors.nc}`, error.message);
    }
}

// Command: flags
async function listFlags() {
    console.log(`${colors.blue}Fetching feature flags...${colors.nc}`);
    
    try {
        const data = await apiCall('/feature_flags');
        const results = data.results || [];
        
        if (results.length === 0) {
            console.log(`${colors.yellow}No feature flags found in this project${colors.nc}`);
            return;
        }
        
        console.log(`${colors.green}Found ${results.length} feature flags${colors.nc}\n`);
        
        for (const flag of results) {
            const name = flag.name || 'N/A';
            console.log(`${colors.cyan}Key:${colors.nc} ${flag.key} | ${colors.yellow}Name:${colors.nc} ${name} | ${colors.blue}Active:${colors.nc} ${flag.active} | ${colors.green}Created:${colors.nc} ${flag.created_at.substring(0, 10)}`);
        }
        
        console.log(`\n${colors.blue}--- Raw JSON ---${colors.nc}`);
        console.log(JSON.stringify(data, null, 2));
        
    } catch (error) {
        console.error(`${colors.red}Error fetching feature flags:${colors.nc}`, error.message);
    }
}

// Command: recordings
async function listRecordings(limit = 10) {
    console.log(`${colors.blue}Fetching session recordings...${colors.nc}`);
    
    try {
        const data = await apiCall('/session_recordings', `limit=${limit}`);
        const results = data.results || [];
        
        if (results.length === 0) {
            console.log(`${colors.yellow}No session recordings found${colors.nc}`);
            return;
        }
        
        console.log(`${colors.green}Found ${results.length} session recordings${colors.nc}\n`);
        
        for (const rec of results) {
            const id = rec.id ? rec.id.substring(0, 20) : 'N/A';
            const distinctId = rec.distinct_id ? rec.distinct_id.substring(0, 20) : 'N/A';
            const startTime = rec.start_time ? rec.start_time.substring(0, 16) : 'N/A';
            const duration = rec.duration || 'N/A';
            console.log(`${colors.cyan}ID:${colors.nc} ${id}... | ${colors.yellow}Distinct ID:${colors.nc} ${distinctId}... | ${colors.blue}Start:${colors.nc} ${startTime} | ${colors.green}Duration:${colors.nc} ${duration}`);
        }
        
        console.log(`\n${colors.blue}--- Raw JSON ---${colors.nc}`);
        console.log(JSON.stringify(data, null, 2));
        
    } catch (error) {
        console.error(`${colors.red}Error fetching session recordings:${colors.nc}`, error.message);
    }
}

// Help
function showHelp() {
    console.log(`
PostHog Analytics Skill - Query your product analytics data

USAGE:
    !posthog <command> [options]

COMMANDS:
    events [options]        Query latest events
      --limit=N             Limit results (default: 10)
      --after=DATE          Filter events after date (YYYY-MM-DD)
      --event=TYPE          Filter by event type

    insights                List all insights/dashboards
    
    dashboards              List all dashboards

    funnel <id>             Get funnel statistics by ID

    persons [options]       Query persons/users
      --limit=N             Limit results (default: 20)
      --search=TERM         Search by email or property

    cohorts                 List all cohorts

    flags                   List all feature flags

    recordings [options]    List session recordings
      --limit=N             Limit results (default: 10)

    help                    Show this help message

EXAMPLES:
    !posthog events --limit=5
    !posthog events --after=2024-01-01 --event=\$pageview
    !posthog persons --search=user@example.com
    !posthog funnel 12345
    !posthog recordings --limit=5

CONFIGURATION:
    Set these environment variables:
    - POSTHOG_API_KEY       Your PostHog API key
    - POSTHOG_PROJECT_ID    Your project ID (default: 43640)
    - POSTHOG_HOST          PostHog host (default: https://eu.posthog.com)
`);
}

// Parse arguments
function parseArgs(args) {
    const result = {};
    for (const arg of args) {
        if (arg.startsWith('--')) {
            const [key, value] = arg.substring(2).split('=');
            result[key] = value || true;
        }
    }
    return result;
}

// Main dispatcher
async function main() {
    const args = process.argv.slice(2);
    const command = args[0] || 'help';
    const parsedArgs = parseArgs(args.slice(1));
    
    switch (command) {
        case 'events':
            await queryEvents(
                parsedArgs.limit || 10,
                parsedArgs.after || '',
                parsedArgs.event || ''
            );
            break;
            
        case 'insights':
            await listInsights();
            break;
            
        case 'dashboards':
            await listDashboards();
            break;
            
        case 'funnel':
            await getFunnel(args[1]);
            break;
            
        case 'persons':
            await queryPersons(
                parsedArgs.limit || 20,
                parsedArgs.search || ''
            );
            break;
            
        case 'cohorts':
            await listCohorts();
            break;
            
        case 'flags':
        case 'feature_flags':
            await listFlags();
            break;
            
        case 'recordings':
        case 'sessions':
            await listRecordings(parsedArgs.limit || 10);
            break;
            
        case 'help':
        case '--help':
        case '-h':
        default:
            showHelp();
            break;
    }
}

main().catch(console.error);
