import re
import os

def migrate_images():
    try:
        # 1. Extract valid image sources from the current index.html (the "source of truth" for images)
        print("Reading index.html...")
        with open('index.html', 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        # Regex to capture src attributes. 
        # Using a simplistic regex assuming the HTML is relatively standard as seen in previous steps.
        # We capture the *value* of the src attribute.
        # Note: This finds ALL images. We assume the count matches or we map as many as possible.
        existing_images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', index_content)
        print(f"Found {len(existing_images)} images in index.html")

        # 2. Read the new content from novo.html
        print("Reading novo.html...")
        with open('novo.html', 'r', encoding='utf-8') as f:
            novo_content = f.read()
            
        new_images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', novo_content)
        print(f"Found {len(new_images)} images in novo.html")

        # 3. Validation
        if len(existing_images) != len(new_images):
            print("WARNING: Image counts do not match!")
            print(f"index.html: {len(existing_images)}")
            print(f"novo.html:  {len(new_images)}")
            print(" proceeding with mapping as many as possible...")
        
        # 4. Replacement Strategy
        # We will split the novo_content by the image tags and reconstruct it, 
        # or use a callback substitution function with an iterator.
        
        img_iter = iter(existing_images)
        
        def replace_src(match):
            try:
                new_src = next(img_iter)
                # match.group(0) is the whole tag. 
                # match.group(1) is the src value.
                # We replace the src value in the full match.
                original_tag = match.group(0)
                old_src = match.group(1)
                return original_tag.replace(old_src, new_src)
            except StopIteration:
                # If we run out of existing images, keep the new one (or handle differently)
                return match.group(0)

        # Regex must match the same pattern used to find them
        result_content = re.sub(r'<img[^>]+src=["\']([^"\']+)["\']', replace_src, novo_content)
        
        # 5. Write to index.html
        print("Writing to index.html...")
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(result_content)
            
        print("Migration complete.")

    except Exception as e:
        print(f"Error during migration: {str(e)}")

if __name__ == "__main__":
    migrate_images()
