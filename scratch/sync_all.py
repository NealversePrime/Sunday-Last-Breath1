import html
import os
import re

print("=" * 60)
print("  SYNCING src/ TO index.html")
print("=" * 60)

with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# 1. Sync engines.js into index.html
with open('src/engines.js', 'r', encoding='utf-8') as f:
    engines_js = f.read()

script_pattern = r'(<script role="script" id="twine-user-script"[^>]*>/\* twine-user-script #1: "engines\.js" \*/\n?)(.*?)(</script>)'
m_script = re.search(script_pattern, index_content, re.DOTALL)
if m_script:
    index_content = index_content[:m_script.start(2)] + engines_js + index_content[m_script.end(2):]
    print(f"[SUCCESS] engines.js ({len(engines_js):,} chars) synchronized into index.html!")
else:
    # Try more generic pattern
    script_pattern_gen = r'(<script role="script" id="twine-user-script"[^>]*>)(.*?)(</script>)'
    m_script_gen = re.search(script_pattern_gen, index_content, re.DOTALL)
    if m_script_gen:
        index_content = index_content[:m_script_gen.start(2)] + engines_js + index_content[m_script_gen.end(2):]
        print(f"[SUCCESS] engines.js ({len(engines_js):,} chars) synchronized into index.html (generic tag)!")
    else:
        print("[ERROR] Could not find twine-user-script in index.html!")

# 2. Sync styles.css into index.html
if os.path.exists('src/styles.css'):
    with open('src/styles.css', 'r', encoding='utf-8') as f:
        styles_css = f.read()

    style_pattern = r'(<style role="stylesheet" id="twine-user-stylesheet"[^>]*>)(.*?)(</style>)'
    m_style = re.search(style_pattern, index_content, re.DOTALL)
    if m_style:
        index_content = index_content[:m_style.start(2)] + styles_css + index_content[m_style.end(2):]
        print(f"[SUCCESS] styles.css ({len(styles_css):,} chars) synchronized into index.html!")
    else:
        print("[WARNING] Could not find twine-user-stylesheet in index.html!")

# 3. Sync passages that exist in src/passages into index.html
passages_dir = 'src/passages'
synced_passages = 0
missing_in_index = 0

if os.path.isdir(passages_dir):
    for filename in os.listdir(passages_dir):
        if filename.endswith('.twee') or filename.endswith('.tw'):
            filepath = os.path.join(passages_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as pf:
                p_text = pf.read()

            # Split multiple passages in a single file if any
            blocks = re.split(r'\n::\s*', '\n' + p_text)
            for b in blocks:
                b = b.strip()
                if not b:
                    continue
                lines = b.split('\n')
                header = lines[0].strip()
                title = re.split(r'[\{\[\n]', header)[0].replace('::', '').strip()
                body = '\n'.join(lines[1:])

                # Search for this passage in index.html
                p_pattern = rf'(<tw-passagedata[^>]*name="{re.escape(title)}"[^>]*>)(.*?)(</tw-passagedata>)'
                m_p = re.search(p_pattern, index_content, re.DOTALL)
                if m_p:
                    escaped_body = html.escape(body, quote=True)
                    index_content = index_content[:m_p.start(2)] + escaped_body + index_content[m_p.end(2):]
                    synced_passages += 1
                else:
                    missing_in_index += 1

print(f"[SUCCESS] Synced {synced_passages} passages into index.html!")
if missing_in_index > 0:
    print(f"[INFO] {missing_in_index} passages not found in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"[SUCCESS] index.html written successfully! Total size: {os.path.getsize('index.html'):,} bytes.")
print("=" * 60)

