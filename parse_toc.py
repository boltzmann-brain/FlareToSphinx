import xml.etree.ElementTree as ET
import os
import errno
import sys


def extractPaths(filename, parent):
"""
Extracts paths of a node's children, and writes paths to the end of the .rst file corresponding to the parent.
For nodes with content, the .rst file should already exist as an end product of the PanDoc conversion.
For nodes with no content, the file has the name of the parent's 'Title' attribute.

"""
	if len(list(parent)): #only put toctree directive if topic has children
		with open(filename, 'a') as index:
			index.write('\n' + '.. toctree::' + '\n' + '   :titlesonly:' + '\n' + '   :caption: Children:'
+ '\n' + '\n')
	for child in parent:
		with open(filename, 'a') as index:
			tocEntry = child.get('Link')
			if tocEntry is None:
				print('This node has children but no content: ' + child.get('Title'))
				tocEntry = '/Content/' + child.get('Title')
			else:
				tocEntry = tocEntry[:-4] #strip file extension
			index.write('   ' + tocEntry + '\n')
					
def extractSubMenus(ancestor):
"""
Sets the filename to be the "Link" attribute of the XML node (if that attribute exists); otherwise the filename is set to the "Title" attribute.

When either one of those attributes is extracted, we run the extractPaths function to find the node's children.

This function is run on all of the top-level topics and their descendants. It won't be run on the root node.

"""

	#get 'link' attribute of node
	file = ancestor.get('Link')
	
	if file is None: #for those parent nodes that are purely navigational, have no content & hence no 'Link' attribute
		file = ancestor.get('Title')
		print('This node has children but no content: ' + file)
		file = 'Content\\' + file + '.rst'
		extractPaths(file, ancestor)
	else: # if 'Link' attribute exists, process string accordingly
		 #replace 'htm' ending with 'rst' & remove starting backslash so that it creates folders relative to program & not relative to root.
		file = file[1:-3] + 'rst'
		
		#replace with Windows separation symbol for paths. Omit this line if you're on a *nix system.
		file = file.replace('/', '\\')

		#get directory that file is in.
		directory = os.path.dirname(file)
		#create directory if it doesn't exist.
		if not os.path.exists(directory):
			try:
				os.makedirs(directory)
			except OSError as error:
				if error.errno != errno.EEXIST:
					raise
		
		#write list of children to rst file
		extractPaths(file, ancestor)	

	for descendant in ancestor.findall("TocEntry"):
		#if there are any children, call recursive function on them.
		extractSubMenus(descendant)

			
#Get tree of nodes by reading from XML file. File name should be first argument in command.
tree = ET.parse(sys.argv[1])

#Get root of XML tree.
root = tree.getroot() #in the .fltoc format the root node is <CatapultToc>.

#extract top-level topics and put their relative paths in index file. In the .fltoc format, these should be the immediate children of root.
extractPaths('index.rst', root)

#run recursive function on all top-level topics (the 'pioneers')
for pioneer in root:
	extractSubMenus(pioneer)