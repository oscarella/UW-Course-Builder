import asyncio
from playwright.async_api import async_playwright

indent_list = []

# wait_for_text() ensures specific element is loaded before performing operations
async def wait_for_text(page, link, text):
    await page.goto(link)
    # Slows application significantly but code "breaks" otherwise
    await page.wait_for_timeout(1000)
    await page.wait_for_load_state('networkidle')
    await page.locator(f'text={text}').first.wait_for(state='visible')

# format_list() returns an ordered list of 'indents' to 'imitate' a bulleted list
#   Elements are of the form <<{num}>> where num represents the degree of indent
async def format_list(loc, indent):
    global indent_list # global var
    list_block = loc.locator('li:not(li li)') # Gathers non-nested <li> elements
    list_block_num = await list_block.count()
    if list_block_num != 0:
        for i in range(list_block_num):
            indent_list.append(f'<<{indent + 1}>>')
            await format_list(list_block.nth(i), indent + 1)

# prettify_subtext() removes tags <*> to display only text within html and incorporates indent_list
async def prettify_subtext(text, indent_list):
    text_len = len(text)
    pretty_text = '' # Final 'prettified' text
    indentation = 0 # index of indent_list
    i = 0 # text[i]
    while i < text_len:
        # Replaces <li> tag, which represents a bullet point, with corresponding symbol
        if (i < text_len - 2 and text[i:(i+3)] == '<li' and indentation < len(indent_list)):
            pretty_text += f' {indent_list[indentation]} '
            indentation += 1
            while(i < text_len and text[i] != '>'):
                i += 1
            i += 1
        # Gets rid of <*>
        elif (text[i] == '<'):
            while(i < text_len and text[i] != '>'):
                i += 1
            i += 1
        # All 'text' is added to pretty_text
        else:
            while(i < text_len and text[i] != '<'):
                pretty_text += text[i]
                i += 1
    return pretty_text

async def main():
    async with async_playwright() as p:

        # Commands to ensure web scraping works when headless mode is True
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-cache', '--max-old-space-size=4096']
        )
        context = await browser.new_context(
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            bypass_csp = True,
            ignore_https_errors = True
        )
        page = await context.new_page()
        await page.set_viewport_size({"width": 1920, "height": 1080})

        # Waterloo Academic Calendar Course page
        await wait_for_text(page, 'https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/courses/', '(WKRPT)')
        # subj_dict[name] = link
        subj_dict = {}
        # Locates subjects: AFM, CS, MATH, ...
        subj_blocks = page.locator('div#__KUALI_TLP li')
        subj_blocks_num = await subj_blocks.count()

        # Populates subj_dict
        for i in range(subj_blocks_num):
            subj_block = subj_blocks.nth(i)
            subj_name = await subj_block.locator('h2').inner_text()
            subj_link = await subj_block.locator('a').get_attribute('href')
            subj_dict[subj_name] = subj_link

        # For each subject ...
        for name,link in subj_dict.items():
            await wait_for_text(page, link, name)
            # course_dict[name] = link
            course_dict = {}
            # Locates courses (Ex. AFM): AFM101, AFM222, ...
            course_blocks = page.locator('div#__KUALI_TLP li')
            course_blocks_num = await course_blocks.count()

            # Populates course_dict
            for i in range(course_blocks_num):
                course_block = course_blocks.nth(i).locator('a')
                course_name = await course_block.inner_text()
                course_link ='https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog' + await course_block.get_attribute('href')
                course_dict[course_name] = course_link

            # For a given course ...
            for c_name, c_link in course_dict.items():
                global indent_list # uses global var
                await wait_for_text(page, c_link, c_name)

                name = await page.title()
                # (DELETE)
                # TEMPORARY COMMAND
                # (DELETE)
                print(name)
                description = ''
                body = ''

                # subheadings represents attributes of a given course
                subheadings = page.locator('div.noBreak')
                subheading_num = await subheadings.count()
                # Iterate over attributes
                for i in range(subheading_num):
                    subheading_i = subheadings.nth(i)
                    subheading_title = await subheading_i.locator('h3').inner_text()
                    indent_list.clear()
                    
                    subheading_text = ''
                    await format_list(subheading_i, 0) # Checks if text is a bulleted list
                    # Subheading text is plain
                    if (len(indent_list) == 0):
                        subheading_text = await subheading_i.locator('div.course-view__pre___2VF54').inner_text()
                    # Subheading text is a list
                    else:
                        subheading_text = await prettify_subtext(await subheading_i.locator('div.course-view__pre___2VF54').inner_html(), indent_list)

                    if subheading_title == 'Description':
                        description = subheading_text
                    else:
                        body += f'[[{subheading_title}]] {subheading_text} '
                
                # (DELETE)
                # TEMPORARY COMMAND
                # (DELETE)
                print(description)
                print(body)
                print()

        await page.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
