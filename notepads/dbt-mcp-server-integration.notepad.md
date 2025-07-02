# dbt MCP Server Integration Notes

- **Integrated:** 2024-06-09 (America/New_York)
- **dbt Project Path:** `.digital_twin/dbt_project`
- **Startup/Shutdown:** Automated via Digital Twin scripts; see logs for status.
- **Config:** See `config.json` > `mcpServers.dbt_mcp`
- **Rules Followed:** bash-safety, stepwise-autonomy, 80-20-prioritization
- **Verification Steps:**
  1. Ensure `dbt_project.yml` exists in the project directory
  2. Run `start_digital_twin.sh` and check for dbt MCP server startup log
  3. Run `stop_digital_twin.sh` and confirm shutdown log
  4. Review `/Users/USERNAME/.digital_twin/logs/dbt_mcp_server.log` for errors
- **Troubleshooting Checklist:**
  - Confirm HTTP transport is enabled (`--transport http` and `FASTMCP_TRANSPORT=http`)
  - Check port 8000 is open: `lsof -iTCP:8000 -sTCP:LISTEN`
  - Test `/docs`, `/`, `/health` endpoints with `curl`
  - If endpoints are not available, check config and logs for transport mode
  - Ensure server logs the HTTP endpoint and transport mode on startup
- **Persistent Note:**
  - MCP servers may default to stdio; always verify transport mode in both config and runtime logs.
- **Reference:** [dbt MCP server docs](https://docs.getdbt.com/blog/introducing-dbt-mcp-server)

- npx-based MCP servers (e.g., memory, sequential_thinking, github, context7) are ephemeral stdio processes, not persistent daemons. This is expected and not an error.
- Health checks should verify server responsiveness (e.g., HTTP endpoint probes), not just process existence. This is proposed as an update to stepwise-autonomy.mdc.
- Notion API MCP server config was fixed (OPENAPI_MCP_HEADERS JSON).
- All configs are now consistent across config.json, .cursor/mcp.json, and claude_desktop_config.json.
- Startup and shutdown scripts are robust, with logging and fallback logic for both Docker and stdio-based servers. 