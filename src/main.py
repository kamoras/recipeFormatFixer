# Recipe Format Fixer
# Version: 0.1.0.0
# Author: Ryan Mack

import sys
import glob
import os

RECIPE_SEPARATOR = "@@@@@\n"
SECTION_SEPARATOR = "|\n"

def writeFile(filePath, recipeName, description, ingredients, instructions):
    with open(filePath, 'a') as f:
        f.write(RECIPE_SEPARATOR)
        f.write(recipeName)
        f.write(SECTION_SEPARATOR)
        f.write(description)
        f.write(SECTION_SEPARATOR)
        f.write(ingredients)
        f.write(SECTION_SEPARATOR)
        f.write(instructions)

def parseFile(filepath):
    file = open(filepath, 'r')
    try:
        lines = file.readlines()
    except UnicodeDecodeError:
        # If we failed to read the file, it may be due to the wrong encoding
        # Windows does utf-16, while Linux does utf-8
        file = open(filepath, 'r', encoding='unicode_escape')
        lines = file.readlines()
    recipeFound = False
    ingredientsFound = False
    instructionsFound = False
    previousLineWasNewLine = False
    chapterFound = False
    servingFound = False
    servingExists = False
    recipeName = ''
    description = ''
    ingredients = ''
    instructions = ''
    for line in lines:
        if line == "\n":
            if previousLineWasNewLine:
                #print("second empty line in a row")
                if recipeFound and chapterFound and not ingredientsFound and not instructionsFound:
                    print("Info: discarding extraneous empty line")
                    continue
                elif not recipeFound or not ingredientsFound or not instructionsFound:
                    print("Error: Reached end of recipe before finding all valid sections")
                else:
                    filepath = chapterName + ".txt"
                    writeFile(filepath, recipeName, description, ingredients, instructions)
                print("Info: End of Recipe")
                # Reset all the local variables
                recipeFound = False
                ingredientsFound = False
                instructionsFound = False
                servingFound = False
                chapterFound = False
                servingExists = False
                recipeName = ''
                description = ''
                ingredients = ''
                instructions = ''
            elif not recipeFound:
                print("recipeName = " + recipeName)
                recipeFound = True
            elif not chapterFound:
                chapterFound = True
            elif not servingFound and servingExists:
                print("serving = " + description)
                servingFound = True
            elif not ingredientsFound:
                print("ingredients = " + ingredients)
                ingredientsFound = True
                servingFound = True # We won't be able to move past ingredients unless we also mark serving as done
            elif not instructionsFound:
                print("instructions = " + instructions)
                instructionsFound = True
            #else:
                #print("empty line separating nothing")

            # If we read a newline then the next iteration will need to know that we just read this
            # (there are 2 new lines to demarcate a new recipe starting)
            previousLineWasNewLine = True
        else:
            # If this line is not new line, then the next iteration will need to know that it was not new line
            # (there are 2 new lines to demarcate a new recipe starting)
            previousLineWasNewLine = False

            # The book name always starts with "Book: "
            if line.startswith("Book:"):
                print("Book")
                #bookName = line.split(" ")[1]
            # The chapter name always starts with "Chapter: "
            elif line.startswith("Chapter:"):
                print("Chapter")
                chapterName = line.split(" ")[1]
            # If it's not one of the known line formats, then we go to the other sections which are in a particular order
            # The recipe name comes first. If we have not yet found the recipe name, this line should be the recipe name
            elif not recipeFound:
                print("Recipe")
                recipeName = line
            # Next after description is ingredients
            elif not ingredientsFound or not servingFound:
                # The amount of servings always starts with "Serves: "
                if line.startswith("Serves:"):
                    print("Serving")
                    # Put the serving size in the description
                    description += line
                    servingExists = True
                else:
                    print("Ingredients")
                    ingredients += line
            # Next after ingredients is instructions
            elif not instructionsFound:
                print("Instructions")
                instructions += line
            else:
                print("Error: Found an unexpected line: " + line)

if __name__ == "__main__":
    print("Welcome to Recipe Format Fixer (version 0.1.0.0), by Ryan Mack")
    totalNumArgs = len(sys.argv)
    if totalNumArgs < 2:
        print("Usage: python main.py [-clean] <filename> {<more filenames>...}")
        print("Note: be sure to use the full file path")

    startIndex = 1
    if sys.argv[1] == "-clean":
        print("Recipe Format Fixer will now begin cleaning past output from the current directory")
        startIndex += 1
        fileList = glob.glob('./*.txt')
        for filePath in fileList:
            try:
                print("Attempting to remove: " + filePath)
                os.remove(filePath)
            except OSError:
                print("Error while deleting file: " + filePath)
            
    print("Recipe Format Fixer will now begin parsing the input files")
    for i in range(startIndex, totalNumArgs):
        print("Now processing: " + sys.argv[i])
        parseFile(sys.argv[i])

    print("Recipe Format Fixer has finished processing your files. The output can be found in the current directory")

