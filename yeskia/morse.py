MORSE_DICT = { 
        'A':'01', 'B':'1000', 'C':'1010', 'D':'100',
        'E':'0', 'F':'0010', 'G':'110', 'H':'0000', 
        'I':'00', 'J':'0111', 'K':'101', 'L':'0100', 
        'M':'11', 'N':'10', 'O':'111', 'P':'0110', 
        'Q':'1101', 'R':'010', 'S':'000', 'T':'1', 'U':'001',
        'V':'0001', 'W':'011', 'X':'1001', 'Y':'1011', 'Z':'1100', 

        '0':'11111', '1':'01111', '2':'00111', '3':'00011', 
        '4':'00001', '5':'00000', '6':'10000', 
        '7':'11000', '8':'11100', '9':'11110',   

        ',':'110011', '.':'010101', '?':'001100', '!':'101011',
        '/':'10010', '-':'100001', '(':'10110', ')':'101101',
        '&':'01000', '$':'0001001'

} 


"""
    Convert text to morse code with 0 = dot and 1 = dash.
    return list containing words, every words is a list contain a string morse code of a charachter 

    convert 'ABC 123' to:
    [
        ['01', '1000', '1010'], # ABC
        ['01111', '00111', '00011'], # 123
    ]

"""
def text_to_morse(text):
    result = []

    # make the text upper case then split into words
    for word in text.upper().split():
        morse_word = [] # empty word list for every word

        # split words into letter
        for char in word:
            c = MORSE_DICT[char] # get morse code from the dictinonary
            morse_word.append(c) # add character in morse to morse_word variable

        result.append(morse_word)

    # return the result
    return result



# for testing 
if __name__ == '__main__':
    # you can change the text in the double quotes to see the result
    print(text_to_morse("Hi there & Hi here!"))
