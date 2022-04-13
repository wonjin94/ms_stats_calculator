from numpy.lib.type_check import imag
import pytesseract
import os
from equip_dict import equip_type_dict
from equip_dict import stat_dict
from equip_dict import potential_dict
from PIL import Image
import cv2
from autocorrect import Speller

# returns full path of tesseract exe file
# func only works on local pc machine with tesseract files
def get_tess_exe_path():
    curr_folder_path = os.path.abspath(os.getcwd())
    full_tesseract_path = os.path.join(curr_folder_path,r'Tesseract-OCR\tesseract')
    return full_tesseract_path

# perform ocr
# input - image
# output -text read by tesseract
def perform_ocr (image) :


    #con = r'--oem 2'
    custom_config = r'--oem 3 --psm 1'
    pytesseract.pytesseract.tesseract_cmd = get_tess_exe_path()
    
    #cropped_img= image.resize((2000,2000))
    #text = pytesseract.image_to_string(cropped_img,lang ="eng" ,config=con)

    text = pytesseract.image_to_string(image,lang ="eng" ,config=custom_config)

    
    return text






# function to check if there is any \n before next text
# returns index after \n
def check_empty_line (text):
    index = 0
    while True:
        if text[:index+1] == "\n":
            index += 1
        else:
            break
    return index

# checks if theres extra space within the text ie - "  "
def check_extra_space(text):
    if text[0] == " ":
        return text[1:]
    else:
        return text

def get_stat_values(text, stat_info,stat):
    values = []

    # get total stat
    #total stat (base stat +..._ \n
    #          ^                  ^
    #        (end)             newline end
    end = 0
    if stat == "Ignored Enemy DEF":
        end = text.find("\n")
    else:
        end = text.find(" ")

    temp = text[:end]
    if temp[-1] == "%":
        temp = temp[:-1]
    values.append(temp)
    newline_end = text.find("\n")
    
    #if has flame
    if stat_info[0]:
        # total stat (base stat + base_stat +flame..._ \n
        #                       ^           ^
        #                      end        next_stat
        end = text.find("+")
        next_stat = text[end+1:].find("+") + end

        # if there is no flame, next_stat should be after newline_end
        if next_stat < newline_end:
            text = text[end+1:]
            end = text.find(" ")
            values.append(text[:end])
            newline_end = text.find("\n")
        else:
            values.append("0")
    else:
        values.append("0")            
    text = text[newline_end+1:]

    return text,values

def process_img_text (input_text):
    # 1st line of text
    # input text = TYPE : equip type\n ....
    end = input_text.find(":")

    # erase everything left of " " after ":" so only equip type is left
    input_text = input_text[end+2:] 
    end = input_text.find("\n")
    # classify equip type from the input text
 
    input_equip_type = input_text[:end]
 
    input_equip_type_info = equip_type_dict[input_equip_type]
    # 1st line of input text is processed
    input_text = input_text[end:]
    
    
    
    # next line of texts to process are stats
    # check empty lines
    values = []
    
    while input_text != "":
    #while input_text != "":
        input_text = input_text[check_empty_line(input_text):]
        # input_text = stat : values....\n...

        # done processing stats, moving on to potentials
        if "Pot" in input_text[:5]:
            break
        
        end = input_text.find(":")

        # get next stat to process
        stat = input_text[:end]
        # remove extra space between stat and ":"
        if stat[-1] == " ":
            stat = stat[:-1]
        
        if stat in stat_dict:
            # : +total stat(base stat +..._ \n
            input_text = input_text[end+3:]
            input_text,value = get_stat_values(input_text,input_equip_type_info,stat)
            temp = []
            temp.append(stat_dict[stat])
            temp.append(value)
            values.append(temp)
        else:
            newline_end = input_text.find("\n")
            input_text = input_text[newline_end+1:]

    # potential line, move to next line to read and process
    newline_end = input_text.find("\n")
    input_text = input_text[newline_end+1:]
 

    output = []
    for i in range(22):
        output.append([0])

    for i in range(3):

        end = input_text.find(":")
        stat = input_text[:end]

        if stat[-1] == " ":
            stat = stat[:-1]
        
        if stat not in potential_dict:
            end = input_text.find("\n")
            input_text = input_text[end+1:]
            if input_text[0]=="\n":
                input_text = input_text[1:]
        else:
            start = input_text.find("+")
            end = input_text.find("%")
        
            value =int(input_text[start+1:end])

            stat_cell_num = potential_dict[stat]-5
            output[stat_cell_num][0] += value
            if i < 2:
                end = input_text.find("\n")
                input_text = input_text[end+1:]
                if input_text[0] == "\n":
                    input_text = input_text[1:]

    
    for i in range(len(values)):
 
        for j in range(len(values[i][0])):
            output[int(values[i][0][j])-5] = [values[i][1][j]]

    print(output)

    col_info = input_equip_type_info[1]
    print("hi")
    return col_info,output






    
