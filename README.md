# Converting a MadCap Flare Project into a Sphinx Project

This project provides scripts for transforming a MadCap Flare project into a Sphinx project. It consists of the following components:
- A Python script, `clean_html.py`, to process Flare's HTML files as follows:
    - Remove non-breaking spaces from the HTML files. ReSt does not like non-breaking spaces.
    - Change the endings of internal links from ".htm" to ".html". While Flare's HTML files have the former endings, Sphinx generates files with ".html" endings. Changing the endings ensures that internal links do not break.
- A batch file, `convert.bat`, that runs `clean_html.py` followed by a [Pandoc](http://pandoc.org/) command on every HTML file in the Flare project's "Contents" folder. The Pandoc command converts the processed HTML files into `.rst` files.
- A Python script, `parse_toc.py`, that reads the Flare project's table of contents (TOC) file, then appends the appropriate `toctree` directives to the RST files that have child topics.

## Prerequisites

The Python scripts use standard Python libraries and the HTML parsing library [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/). If you are using [pip](https://pip.pypa.io/en/stable/installing/) as your Python package manager, you can install the latest version of Beautiful Soup using the command `pip install beautifulsoup4`. The scripts were tested on Python 3, but they should run fine on Python 2---I don't think I used anything specific to Python 3.

You should [install Pandoc](http://pandoc.org/installing.html) in order to run `convert.bat`. We use a batch script because Flare runs on Windows only; however, the commands in the script are exceedingly simple, so it should be trivial to convert the batch file into a bash script.

In `parse_toc.py`, the `extractSubMenus()` function assumes that file paths are in Windows, so the `\` separator is used. If you are on a *nix system, you'll want to edit the lines that implement this separator.

### Folder Structure

The scripts assume the following folder structure for your Sphinx project:

````
ProjectFolder
|   index.rst (top level of TOC; will be generated here by default)
|   convert.bat
|   clean_html.py
|   parse_toc.py
|   .fltoc file (Flare table of contents)
|---Contents folder (copied from Flare project)
|      Flare HTML and generated RST files
````
In short,
- The project folder should contain all the conversion scripts.
- You should copy your Flare project's `Contents` folder into the project folder.
- The scripts will generate all the `.rst` files in the same subfolders as their corresponding HTML files. The only exception is the file containing the top levels of the TOC, `index.rst`. This will be stored directly in the project folder.

## Parent Nodes without Content

Flare projects allow for parent nodes in the TOC that have no content themselves, but that when expanded, contain child topics. `parse_toc.py` currently does not have a foolproof way of handling such nodes. For parent nodes with content, it relies on the `Link` attribute in the `.fltoc` file. Contentless parent nodes do not have this attribute, so `parse_toc.py` relies on the `Title` attribute for these nodes, and writes the `.rst` files corresponding to these nodes directly under the "Contents" folder. However, for reasons I haven't had time to understand yet, some contentless nodes fail to be replicated correctly this way.

At present, `parse_toc.py` also prints to the console the titles of contentless parent nodes, so that you can have a list of them, manually check which ones aren't converted by the script, and manually convert them yourselves. If you do not have any contentless parent nodes in your project (i.e. if all `TocEntry` elements in your `.fltoc` file have the `Link` attribute), there is no need for manual conversion.

## toctree Options

The default script inserts a `titlesonly` option under the `toctree` directives it creates. This imitates Flare's TOC structure, since Flare does not include topic subheaders in its TOCs. To remove this option or to add more options (`hidden`, captions, etc.), edit the first part of the `extractPaths()` function.

The script also inserts the `toctree` directive at the end of the file. If you want the local TOCs to be displayed elsewhere in the document, you will have to edit `extractPaths()`. Note that you cannot put the `toctree` directive *before* the first header in a document---it messes up Sphinx's interpretation of the TOC structure.

## Conversion Procedure

1. Create the folder for your Sphinx project and put the scripts from this Git repository in it. You can simply clone the repository and use its folder as the Sphinx project folder.
2. Copy the `Contents` folder of your Flare project into your Sphinx project folder. Make sure to copy the `Contents` folder that is in the same folder as the `.flprj` file. Do not copy the `Contents` folder that is under the `Output` folder, as the latter will contain extra styling elements.
3. Copy the desired Flare table of contents into your Sphinx project folder. This should be an `.fltoc` file within the `Project\TOCs` subfolder of your Flare project folder.
4. In the Windows Powershell or command terminal, run `convert.bat`.
5. In the Windows Powershell or command terminal, run the TOC parsing script by typing `python parse_toc.py yourFlareTOCFile`. Replace `yourFlareTOCFile` with the name of the `.fltoc` file that contains your TOC structure.
6. You should now have an `index.rst` file that contains a `toctree` directive with the top-level topics in your TOC. Your `Contents` folder will now contain an RST file for each HTML file. RST files for topics with children will have the appropriate `toctree` directive at the end of each file.
7. You can test the new TOC by running the `sphinx-quickstart` command in the Sphinx project folder, and following [the instructions](http://www.sphinx-doc.org/en/master/usage/quickstart.html) for setting up a quick test build.

