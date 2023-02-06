# Importing required libraries from selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By

# Importing exception handling libraries
from selenium.common.exceptions import TimeoutException

def get_product_links(base_url, brand_list):
    # Initialize an empty list to store the links
    links = []
    
    # Loop through each brand in the list
    for brand in brand_list:
        # Format the base URL with the current brand
        url = base_url.format(brand)
        
        # Initialize the webdriver
        browser = webdriver.Chrome()
        
        # Navigate to the URL
        browser.get(url)
        
        # Counter to keep track of the number of pages processed
        counter = 0
        
        # Loop until all pages have been processed
        while True:
            # If all pages have been processed, break out of the loop
            if counter == 1:
                break
                
            try:
                # Find the next button
                next_button = browser.find_element(By.CLASS_NAME, "s-pagination-item.s-pagination-next")
                
                # If the next button is not enabled, break out of the loop
                if not next_button.is_enabled():
                    break
                    
                # Find all the link elements on the page
                link_elements = browser.find_elements(By.CLASS_NAME, "a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
                
                # Add the href attribute of each link element to the links list
                links.extend([link.get_attribute('href') for link in link_elements])
                
                # Wait for the next button to be clickable
                browser.implicitly_wait(25)
                
                # Click the next button
                next_button.click()
                
                # Increment the counter
                counter += 1
                
            # If an exception is raised, break out of the loop
            except:
                break
                
    # Close the webdriver
    browser.close()
    
    # Return the list of links
    return links


#url with base structure for scraping headphones
base_url='https://www.amazon.in/s?k=headphones&i=electronics&bbn=1388921031&rh=n%3A1388921031%2Cp_89%3A{}&dc&page=1&crid=26YCJ7VB7YLJ4&qid=1675167468&rnid=3837712031&sprefix=%2Caps%2C1567&ref=sr_pg_'
# List of Brand names to search for
brand_list=['boAt',  'Boult Audio', 'Mivi', 'JBL', 'ZEBRONICS',  'SONY', 'Ubon',  'Jabra', 'GoSale', 'Shop Reals']


#Calling the function to scrap all the product links of the brands above and storing it in a list
links=get_product_links(base_url,brand_list)

# Removing duplicate links
links=list(set(links))



# Lists to store product information
product_title=[]
product_price=[]
brand_name=[]
product_model=[]
product_colour=[]
product_form_factor=[]
product_connector_type=[]
product_Connectivity=[]



# Removing duplicate links
merged_list=list(set(merged_list))

# Function to extract product specifications
def extract_specifications(rows):
    # Join the elements of the list into a single string
    for row in rows:
        try:
            # Finding the product specifications
            cols = row.find_elements(By.XPATH, '//span[@class="a-size-base po-break-word"]')
            cols = [col.text for col in cols]
        except:
            cols='N.A'
    return cols

# Looping through each product link

for links in merged_list:

    browser.get(links)
    elem1=browser.find_element(By.XPATH,'//span[@class="a-size-large product-title-word-break"]')
    text=elem1.text
    product_title.append(text)

    try:
        elem2=browser.find_element(By.XPATH,'//span[@class="a-price-whole"]')
        text2=elem2.text
    except:
        text2='N.A'
        pass
        
  
    product_price.append(text2)
    try:
        elem3 = browser.find_element(By.XPATH,'//table[@class="a-normal a-spacing-micro"]')
        rows = elem3.find_elements(By.TAG_NAME, "tr")
        col=extract_specifications(rows)


        
    except:
        text3='N.A'
        pass
    
    cols=extract_specifications(rows)
    if len(cols)==5:
        brand_name.append(cols[0])
        product_model.append(cols[1])
        product_colour.append(cols[2])
        product_form_factor.append(cols[3])
        product_connector_type.append(cols[4])
    else:    
        brand_name.append('N.A')
        product_model.append('N.A')
        product_colour.append('N.A')
        product_form_factor.append('N.A')
        product_connector_type.append('N.A')



        
        

#Converting Lists to Data Frame
df=pd.DataFrame([product_title,product_price,brand_name,product_model,product_colour,product_form_factor,product_connector_type])
df=df.transpose()
df.columns = ['Title', 'Price','Brand','Model Name','Colour','Form factor','Connector Type'.'Connectivity']


#Converting List to CSV
df.to_csv('Amazon_headphones.csv', index=False) 
