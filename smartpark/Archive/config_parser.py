"""A class or function to parse the config file and return the values as a dictionary.

"""
import json
from pathlib import Path

def parse_config(config_file: str,site_name: str) -> dict:
    """Parse the config file and return the values as a dictionary"""
    #  CONFIG_FILE = "samples_and_snippets\\config2.json"

  
    # Ensure the config file exists
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
  
    #open JSON file
    with open(config_file, "r") as f:
        carparks_loaded = json.load(f)

    # Clean whitespace in keys
    carpark_dict = {k.strip(): v for k, v in carparks_loaded.items()}
    cleaned_dict = carpark_dict 

    # check for the dictionary for bays in king street
  #  site = site_name.strip()      
  #  total_spaces = carpark_dict.get(site,"Is not a carpark")
    a = carpark_dict["CarParks"]

    for park in a:
        location= park.get("location","").strip().lower() == site_name
        if (
           park.get("location","").strip().lower() == site_name.lower()
           or park.get("name", "").strip().lower() == site_name.lower()
        ):         
            #return only the relevant information    
            return {"location":park.get("location","Unknown"),
                    "total_spaces":park.get("total_spaces",0),
                    "unuseable_spaces":park.get("unuseable_spaces",0),
                    "log_file":park.get("log_file","carpark_log.txt")
                    }
        
    #if not return found
    return {"error": f"No CarPark Found for site '{site}"}
            
    #return {'location': 'TBD', 'total_spaces': 0, 'log_file':'carpark_log.txt' }
    return {'location': site, 'total_spaces' : total_spaces, 'log_file': log_file }

#CNFIG_FILE = "samples_and_snippets\\config2.json"
#CONFIG_FILE = "samples_and_snippets\\Carpark_config.json"


#if __name__ == "__main__":
    #result = parse_config("Carpark_config.json","King Street")
    #result = parse_config("samples_and_snippets\\config2.json","King Street")
    print({'location': 'TBD', 'total_spaces': 0, 'log_file':'carpark_log.txt'})
    print(parse_config(CONFIG_FILE,"Queen Street"))
    #print(parse_config(CONFIG_FILE,"Queen Street"))

    # print(parse_config("samples_and_snippets\\config2.json")) #  Visual sudiio import

    #cfg_data = parse-config ("samples_and_snippets\\config2.json")
    #print(cfg_data)

    #Can now call any item from the dictionary
