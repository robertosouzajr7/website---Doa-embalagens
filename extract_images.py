import re

def extract_images(filename, outfile):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            # More robust regex to capture src
            images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
            outfile.write(f"--- {filename} ({len(images)} images) ---\n")
            for i, img in enumerate(images):
                outfile.write(f"{i}: {img}\n")
            outfile.write("\n")
    except Exception as e:
        outfile.write(f"Error reading {filename}: {str(e)}\n")

with open('image_report.txt', 'w', encoding='utf-8') as f:
    extract_images('index.html', f)
    extract_images('novo.html', f)
