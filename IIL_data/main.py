from utils import *

def main(usecase):
 
  filepath = '/content/drive/MyDrive/IIL/' + usecase + '.csv'   # provide path of the csv file storing tags and other data
  df = pd.read_csv(filepath, encoding= 'unicode_escape')
  
  newfilepath = add_human_description(filepath) # this function allows to add human description to the tags and returns path of new csv file

  df = pd.read_csv(newfilepath)

  create_json_new(newfilepath, usecase)  # creates the json responses for the tags and usecase


if __name__ == '__main__':
  main()

