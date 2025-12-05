#!/usr/bin/env python3
"""
Convert .eml files to Markdown format
"""

import email
import base64
import re
import os
import subprocess
import sys
from email.header import decode_header
from pathlib import Path

# Check and install dependencies
def check_dependencies():
    """Check if required packages are installed and install if missing"""
    required_packages = ['html2text']
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing missing dependency: {package}")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', package])
                print(f"Successfully installed {package}")
                # Reload sys.path to pick up newly installed packages
                import site
                import importlib
                importlib.reload(site)
            except subprocess.CalledProcessError as e:
                print(f"Error installing {package}: {str(e)}")
                sys.exit(1)

# Run dependency check
check_dependencies()

import html2text

def decode_email_header(header):
    """Decode email headers that might be encoded"""
    if header is None:
        return ''
    decoded_parts = decode_header(header)
    decoded_string = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            if encoding:
                decoded_string += part.decode(encoding)
            else:
                decoded_string += part.decode('utf-8', errors='ignore')
        else:
            decoded_string += part
    return decoded_string

def extract_email_content(msg):
    """Extract text content from email message"""
    body_text = ''
    body_html = ''

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            
            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                charset = part.get_content_charset() or 'utf-8'
                content = part.get_payload(decode=True)
                if content:
                    try:
                        body_text = content.decode(charset, errors='ignore')
                    except:
                        body_text = str(content)
                    break  # Use first plain text part
                        
            elif content_type == 'text/html' and 'attachment' not in content_disposition and not body_text:
                charset = part.get_content_charset() or 'utf-8'
                content = part.get_payload(decode=True)
                if content:
                    try:
                        body_html = content.decode(charset, errors='ignore')
                    except:
                        body_html = str(content)
    else:
        content = msg.get_payload(decode=True)
        if content:
            content_type = msg.get_content_type()
            charset = msg.get_content_charset() or 'utf-8'
            try:
                if content_type == 'text/html':
                    body_html = content.decode(charset, errors='ignore')
                else:
                    body_text = content.decode(charset, errors='ignore')
            except:
                body_text = str(content)

    # Convert HTML to text if we have HTML but no plain text
    if body_html and not body_text:
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0  # Don't wrap lines
        body_text = h.handle(body_html)

    return body_text

def clean_email_body(body_text):
    """Clean up the email body text"""
    if not body_text:
        return ""
    
    # Remove excessive newlines
    body_text = re.sub(r'\n{3,}', '\n\n', body_text)
    
    # Remove leading/trailing whitespace
    body_text = body_text.strip()
    
    return body_text

def convert_eml_to_md(eml_file_path, output_dir):
    """Convert a single .eml file to Markdown"""
    try:
        # Read the .eml file
        with open(eml_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw_email = f.read()

        # Parse the email
        msg = email.message_from_string(raw_email)

        # Extract headers
        from_addr = decode_email_header(msg.get('From'))
        to_addr = decode_email_header(msg.get('To'))
        cc_addr = decode_email_header(msg.get('CC'))
        subject = decode_email_header(msg.get('Subject'))
        date = decode_email_header(msg.get('Date'))

        # Extract body
        body_text = extract_email_content(msg)
        body_text = clean_email_body(body_text)

        # Create Markdown content
        md_content = f"""# {subject}

**From:** {from_addr}  
**To:** {to_addr}  
"""
        
        if cc_addr:
            md_content += f"**CC:** {cc_addr}  \n"
        
        md_content += f"**Date:** {date}  \n\n"
        
        md_content += "---\n\n"
        md_content += body_text

        # Create output filename
        eml_filename = Path(eml_file_path).stem
        md_filename = f"{eml_filename}.md"
        md_file_path = os.path.join(output_dir, md_filename)

        # Write Markdown file
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"Converted: {eml_file_path} -> {md_file_path}")
        return True

    except Exception as e:
        print(f"Error converting {eml_file_path}: {str(e)}")
        return False

def main():
    """Main function to convert all .eml files from email/raw to email/ai"""
    # Get the script directory and project root
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.parent
    
    # Define directory structure relative to project root
    raw_dir = project_root / "email" / "raw"
    ai_dir = project_root / "email" / "ai"
    processed_dir = project_root / "email" / "processed"
    
    # Create directories if they don't exist
    raw_dir.mkdir(parents=True, exist_ok=True)
    ai_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    print(f"Directory structure ready:")
    print(f"  Raw: {raw_dir}")
    print(f"  AI: {ai_dir}")
    print(f"  Processed: {processed_dir}")
    
    # Find all .eml files in raw directory
    eml_files = list(raw_dir.glob("*.eml"))

    if not eml_files:
        print(f"No .eml files found in {raw_dir}")
        return

    print(f"\nFound {len(eml_files)} .eml file(s) to convert")

    # Convert each file
    converted_count = 0
    for eml_file in eml_files:
        if convert_eml_to_md(str(eml_file), str(ai_dir)):
            # Move processed .eml file to processed directory
            processed_path = processed_dir / eml_file.name
            try:
                eml_file.rename(processed_path)
                print(f"Moved to processed: {eml_file.name}")
                converted_count += 1
            except Exception as e:
                print(f"Error moving {eml_file.name} to processed: {str(e)}")

    print(f"\nConversion completed! {converted_count}/{len(eml_files)} files successfully processed")

if __name__ == "__main__":
    main()
