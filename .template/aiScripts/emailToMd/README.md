# Email to Markdown Converter

## Purpose
Convert `.eml` email files to Markdown format for AI processing and analysis.

## Usage

**Run from project root directory:**

```bash
python3 ".template/aiScripts/emailToMd/eml_to_md_converter.py"
```

The script will:
1. Create `email/raw/`, `email/ai/`, and `email/processed/` directories in project root (if they don't exist)
2. Read all `.eml` files from `email/raw/`
3. Convert them to Markdown format
4. Save converted files to `email/ai/` as `.md` files
5. Move processed `.eml` files to `email/processed/`

## Directory Structure

Script automatically creates these directories in the **project root**:
- `email/raw/` - Place original `.eml` files here
- `email/ai/` - Converted `.md` files output here
- `email/processed/` - Processed `.eml` files moved here

## Output Format

Converted Markdown files include:
- Subject (as heading)
- From, To, CC, Date metadata
- Email body content (HTML converted to Markdown)

## Notes for AI Agents

1. **Always run from project root**: Script must be executed from the project root directory, not from within `.template/aiScripts/emailToMd/`
2. **Auto-creates directories**: Script automatically creates `email/raw/`, `email/ai/`, and `email/processed/` in project root
3. **After conversion**: Verify `.md` files are in `email/ai/` and original `.eml` files are moved to `email/processed/`
4. **Error handling**: Check script output for any conversion errors
5. **Dependencies**: Script auto-installs required packages (html2text)
