#!/usr/bin/env python3
"""
state_manager.py - Manages .lumina.state file for project tracking

This module provides functions to create, read, and update the project state file.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


def get_state_file_path() -> Path:
    """Get the path to the .lumina.state file in the project root."""
    # Assume this script is in core/aiScripts/, so project root is two levels up
    return Path(__file__).parent.parent.parent / ".lumina.state"


def create_state_file(
    project_name: str,
    customer_name: str,
    your_name: str,
    git_hooks_installed: bool = False,
    dependencies_installed: bool = False,
    directories_created: bool = False,
    mcp_configured: bool = False
) -> None:
    """
    Create a new .lumina.state file with initial values.
    
    Args:
        project_name: Name of the project
        customer_name: Name of the customer
        your_name: Name of the user initializing the project
        git_hooks_installed: Whether git hooks are installed
        dependencies_installed: Whether dependencies are installed
        directories_created: Whether required directories are created
        mcp_configured: Whether MCP servers are configured
    """
    now = datetime.now(timezone.utc).isoformat()
    
    state = {
        "version": "1.0",
        "initialized": True,
        "project_name": project_name,
        "customer_name": customer_name,
        "your_name": your_name,
        "created_at": now,
        "last_updated": now,
        "operations": {
            "last_email_processed": None,
            "last_summary_generated": None,
            "emails_processed_count": 0,
            "git_hooks_installed": git_hooks_installed
        },
        "health": {
            "dependencies_installed": dependencies_installed,
            "directories_created": directories_created,
            "mcp_configured": mcp_configured
        }
    }
    
    state_file = get_state_file_path()
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)


def read_state() -> Optional[Dict[str, Any]]:
    """
    Read the current state from .lumina.state file.
    
    Returns:
        Dictionary with state data, or None if file doesn't exist or is malformed
    """
    state_file = get_state_file_path()
    
    if not state_file.exists():
        return None
    
    try:
        with open(state_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def update_state(updates: Dict[str, Any]) -> bool:
    """
    Update specific fields in the state file, preserving unknown keys.
    
    Args:
        updates: Dictionary with keys to update (supports nested keys with dot notation)
                 Example: {"operations.emails_processed_count": 5}
    
    Returns:
        True if successful, False if state file doesn't exist or is malformed
    """
    state = read_state()
    
    if state is None:
        return False
    
    # Update last_updated timestamp
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    
    # Apply updates
    for key, value in updates.items():
        if '.' in key:
            # Handle nested keys like "operations.emails_processed_count"
            parts = key.split('.')
            target = state
            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            target[parts[-1]] = value
        else:
            # Top-level key
            state[key] = value
    
    # Write back to file
    state_file = get_state_file_path()
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        return True
    except IOError:
        return False


def increment_email_count() -> bool:
    """
    Increment the emails_processed_count and update last_email_processed timestamp.
    
    Returns:
        True if successful, False otherwise
    """
    state = read_state()
    
    if state is None:
        return False
    
    now = datetime.now(timezone.utc).isoformat()
    current_count = state.get("operations", {}).get("emails_processed_count", 0)
    
    return update_state({
        "operations.emails_processed_count": current_count + 1,
        "operations.last_email_processed": now
    })


def update_summary_timestamp() -> bool:
    """
    Update the last_summary_generated timestamp.
    
    Returns:
        True if successful, False otherwise
    """
    now = datetime.now(timezone.utc).isoformat()
    return update_state({
        "operations.last_summary_generated": now
    })


def display_state() -> None:
    """
    Display the current project state in a human-readable format.
    Designed to be called from go.sh menu.
    """
    state = read_state()
    
    if state is None:
        print("\033[1;33m📊 Project Status: Not Initialized\033[0m")
        print("   Run 'Initialize Project' to get started")
        return
    
    # Check if state file is from before state tracking
    if not state.get("initialized", False):
        print("\033[1;33m📊 Project Status: Unknown\033[0m")
        print("   Project may have been initialized before state tracking was added.")
        print("   Re-run initialization to enable state tracking.")
        return
    
    # Display project info
    print("\033[1;34m📊 Project Status:\033[0m")
    print(f"   Project: {state.get('project_name', 'Unknown')}")
    print(f"   Customer: {state.get('customer_name', 'Unknown')}")
    
    # Display initialization info
    created = state.get('created_at')
    if created:
        try:
            created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
            print(f"   Initialized: \033[0;32m✓\033[0m ({created_dt.strftime('%Y-%m-%d')})")
        except ValueError:
            print(f"   Initialized: \033[0;32m✓\033[0m")
    
    # Display operations stats
    ops = state.get('operations', {})
    email_count = ops.get('emails_processed_count', 0)
    if email_count > 0:
        print(f"   Emails Processed: {email_count}")
    
    # Display last updated (humanized)
    last_updated = state.get('last_updated')
    if last_updated:
        try:
            updated_dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            delta = now - updated_dt
            
            if delta.total_seconds() < 3600:
                minutes = int(delta.total_seconds() / 60)
                print(f"   Last Updated: {minutes} minute{'s' if minutes != 1 else ''} ago")
            elif delta.days == 0:
                hours = int(delta.total_seconds() / 3600)
                print(f"   Last Updated: {hours} hour{'s' if hours != 1 else ''} ago")
            else:
                days = delta.days
                print(f"   Last Updated: {days} day{'s' if days != 1 else ''} ago")
        except ValueError:
            pass
    
    print()  # Empty line for spacing


if __name__ == "__main__":
    # If called directly, display the state
    display_state()
