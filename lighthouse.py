"""
Project Name: Lighthouse
Description: This is an admin script which will take a zip file and create a directory structure from its contents
Author: Ian Bartlow
"""

from zipfile import ZipFile  # to process the zip file
import os  # for manipulating directories/files
import re  # regular expressions for parsing  metadata.xml
from tkinter import simpledialog  # for the zip file dialog box
import tkinter as tk  # for our tkinter root
from tkinter.messagebox import askyesno  # for our overwrite prompt
import shutil  # a library for performing high level directory operations
from tkinter import *
import webbrowser
import xml.etree.ElementTree as ET  # used to parse metadata.xml


class Lighthouse:
    def __init__(self):
        if os.path.exists("C:/lighthouse/documents/tempDir"):
            shutil.rmtree("C:/lighthouse/documents/tempDir")

        # creates the initial gui
        self.root = Tk()
        self.root.geometry("800x500")
        button = Button(
            self.root, text="Upload", command=lambda: Lighthouse.upload(self)
        )
        button2 = Button(
            self.root, text="Delete", command=lambda: Lighthouse.deleteHelper(self)
        )

        button.pack()
        button2.pack()
        self.root.mainloop()

        # deletes the temp directory for clean up
        if os.path.exists("C:/lighthouse/documents/tempDir"):
            shutil.rmtree("C:/lighthouse/documents/tempDir")

    """
    args: self, metadataPath
    metadataPath - the path to the metadata file inside each product directory
    returns: newPath
    newPath - the path constructed from the information we parse via regex in each metadata.xml file
    format: /productName/versionNumber/publicationName/language
    """

    def createPath(self, metadataPath):
        tree = ET.parse(metadataPath)
        root = tree.getroot()
        newPath = []
        newPath.append(root.find("product-name").text)
        newPath.append(root.find("publication-version").text)
        newPath.append(root.find("publication-name").text.replace("\n", " "))
        newPath.append(root.find("language").text)

        return newPath

    """
    creates the directory structure based on elements in the folderPath array
    args: folderPath, dirIndex, basePath
    folderPath - the path returned by createPath() split
    dirIndex - keeps track of where we are in our tempDir
    basePath - the default path we want to writee to
    copies contents from our tempDir to the permanent directory
    """

    def createDirectory(self, folderPath, dirIndex, basePath):
        newDir = "C:/lighthouse/documents/"
        docPath = newDir

        # create the html file for website index
        htmlIndex = open(newDir + "/" + "index.html", "a")
        index2 = open(newDir + "/index2.html", "a")

        # builds the path to test for existence later
        for folder in folderPath:
            docPath = docPath + "/" + folder

        # if it already exists, give user a gui button to choose to overwrite
        # if it does not exist, create it
        if os.path.exists(docPath):
            userAnswer = askyesno(
                title="Overwrite Confirmation",
                message=""
                + docPath
                + " already exists, would you like to overwrite it?",
            )

            # if user says yes, delete and remake
            if userAnswer:
                newDir = "C:/lighthouse/documents/"

                # delete the content in the path to be overwritten
                for file in os.listdir(docPath):
                    thing = os.path.join(docPath, file)

                    if os.path.isfile(thing):
                        os.remove(thing)
                    elif os.path.isdir(thing):
                        shutil.rmtree(thing)

                # recreates the files, making sure to allow for different versions of the same product etc.
                for folder in folderPath:
                    newDir = os.path.join(newDir, folder)
                    if os.path.isdir(newDir):
                        continue
                    else:
                        os.mkdir(newDir)

                if dirIndex >= 0:
                    sourceDir = basePath + "/" + os.listdir(basePath)[dirIndex]
                    shutil.copytree(sourceDir, newDir, dirs_exist_ok=True)
                else:
                    sourceDir = "C:/lighthouse/documents/tempDir"
                    shutil.copytree(sourceDir, newDir, dirs_exist_ok=True)

        else:
            # create the directory
            for folder in folderPath:
                newDir = os.path.join(newDir, folder)
                if os.path.isdir(newDir):
                    continue
                else:
                    os.mkdir(newDir)

            if dirIndex >= 0:
                sourceDir = basePath + "/" + os.listdir(basePath)[dirIndex]
                shutil.copytree(sourceDir, newDir, dirs_exist_ok=True)
            else:
                sourceDir = "C:/lighthouse/documents/tempDir"
                shutil.copytree(sourceDir, newDir, dirs_exist_ok=True)
            # create the html index for the website, only does it when new
            # things are added
            htmlIndex.write(
                '<a href="'
                + docPath
                + "//index.html"
                + '" target="display" style="font-size: 18; color: black; font-family: sans-serif;">'
                + folderPath[0]
                + " "
                + folderPath[3]
                + "</a><br><br>"
            )
            if os.path.isfile(newDir + "/index.html"):
                indexCopy = open(newDir + "/index.html")
                for line in indexCopy.readlines():
                    index2.write(line)

        htmlIndex.close()
        index2.close()

    # helper function for the delete window
    def deleteHelper(self):
        # creates a box allowing multiple selections
        listbox = Listbox(self.root, width=100, height=20, selectmode=MULTIPLE)
        index = 1

        # builds the selections in the box
        for folder in os.listdir("C:\lighthouse\documents"):
            if folder == "index.html" or folder == "index2.html":
                continue
            else:
                path = "C:\lighthouse\documents" + "\\" + folder
                subFolders = Lighthouse.delete(self, path)
                listbox.insert(index, subFolders[2])

        # event handler for our selection box
        # lets the user select which things they want to delete, deletes them from the computer
        # and from the box itself
        def selected_item():
            indicies = []
            for i in listbox.curselection():
                prodDir = (
                    "C:\lighthouse\documents" + "\\" + listbox.get(i).split("\\")[3]
                )
                shutil.rmtree(prodDir)
                indicies.append(i)

            # adjust the html file
            htmlIndex = open("C:/lighthouse/documents/index.html", "w")
            for folder in os.listdir("C:\lighthouse\documents"):
                if folder == "index.html" or folder == "index2.html":
                    continue
                else:
                    path = "C:\lighthouse\documents" + "\\" + folder
                    subFolders = Lighthouse.delete(self, path)
                    displayName = path.split("\\")
                    htmlIndex.write(
                        '<a href="'
                        + subFolders[2]
                        + '" target="display" style="font-size: 18; color: black; font-family: sans-serif;">'
                        + displayName[3]
                        + "</a><br><br>"
                    )

            htmlIndex.close()
            for i in indicies:
                listbox.delete(i)

            deleteSelection.pack_forget()
            listbox.pack_forget()

        # adds the button/box to root
        deleteSelection = Button(
            self.root, text="Delete Selected", command=selected_item
        )
        listbox.pack()
        deleteSelection.pack()

    """
     deletes a directory
     args: dirName
     dirName - path of the directory to be deleted
    """

    def delete(self, dirName):
        # recursively finds the subdirectories for a given directory
        subFolders = [f.path for f in os.scandir(dirName) if f.is_dir()]
        for dirName in list(subFolders):
            subFolders.extend(Lighthouse.delete(self, dirName))
        return subFolders

    # event handler for upload button
    def upload(self):
        # get the zip location from the user
        userInput = simpledialog.askstring(
            title="Upload Zip File", prompt="Enter Zip File Path:"
        )

        # unzip the userInput into a temporary directory
        try:
            with ZipFile(userInput, "r") as zipObject:
                directory = "tempDir"
                parentDir = "C:\\lighthouse\\documents"
                path = os.path.join(parentDir, directory)
                os.mkdir(path)
                zipObject.extractall(path)
            thing = path
            path += "\\" + str(os.listdir(path)[0])

        # if the path does not exist
        except FileNotFoundError:
            tk.messagebox.showwarning(
                title="File Not Found",
                message="File not found, try restarting "
                + "and enter a different path",
            )

        # if zip is a directory of directories, do this
        if os.path.isdir(path):
            basePath = path
            dirIndex = 0
            tempDir = os.listdir(path)
            for folder in tempDir:
                path += "\\" + str(folder) + "\\metadata_info.xml"
                Lighthouse.createDirectory(
                    self, Lighthouse.createPath(self, path), dirIndex, basePath
                )
                path = basePath
                dirIndex += 1
        # if the zip contains no directories and just 1 metadta file
        else:
            tempDir = os.listdir(thing)
            basePath = thing
            Lighthouse.createDirectory(Lighthouse.createPath(path), -2, basePath)
        if os.path.exists("C:/lighthouse/documents/tempDir"):
            shutil.rmtree("C:/lighthouse/documents/tempDir")


def main():
    webbrowser.open("c:\lighthouse\English\ProjectLighthouseDirectory.html")
    lighthouse = Lighthouse()


if __name__ == "__main__":
    main()
