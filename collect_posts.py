from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

SLEEPTIME = 1.5
NUMPAGES = 1000;

#https://www.linkedin.com/company/international-paper?trk=company_logo

def GetPosts():

    posts = {}

    url = input('Enter the company name on linkedIn (ex: z1-solutions): ')

    url = url.replace(' ', '-')
    #username = input('Enter your linkedin email (must be admin of company to view followers): ')
    #password = input('Enter your password: ')
    
    
    #wd.get('https://www.linkedin.com')


    #email = wd.find_element_by_id('login-email')
    #pword = wd.find_element_by_id('login-password')

    #email.send_keys(username)
    #pword.send_keys(password)

    #Linkedin has very inconsistent html tags...so we have to check both - otherwise it crashes
    #try:
      #  wd.find_element_by_name("submit").click()
   # except:
      #  wd.find_element_by_id("login-submit").click()

   # if wd.current_url != 'https://www.linkedin.com/nhome/':
      #  print('log-in credentials incorrect!')
     #   wd.quit()
      #  return

    wd = webdriver.Firefox()

    try:
        #wd.get('https://www.linkedin.com/company/z1-solutions?trk=top_nav_home')
        wd.get('https://www.linkedin.com/company/' + url + '?trk=company_logo')
    except:
        print('Company URL does not exist!')
        wd.quit()
        return

    fn = url + '-names.txt'

    run = True

    #Keep running, adding names to list and clicking 'next' until you run out of pages
    while run == True:

        lastHeight = 0

        print('run = ' + str(run))

        for i in range(NUMPAGES):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SLEEPTIME)

            newHeight = wd.execute_script("return document.body.scrollHeight")
            print(lastHeight)
            print(newHeight)
            if newHeight == lastHeight:
                print('sbfkhjdfbdfsfdb')
                run = False
                break

            lastHeight = newHeight

            source = wd.find_element_by_id('body').get_attribute('outerHTML')

            print('BEFORE SOUP')

            soup = BeautifulSoup(source, 'html.parser')
           
            for p in soup.findAll('div', attrs={'class':'feed-content'}):
                print('in soup')
                days = p.find('a', attrs={'class':'nus-timestamp'})
                num = int(days.getText().split()[0])
                t = days.getText().split()[1]

                if t == 'hours' or t =='minutes' or t == 'day' or (t == 'days' and num < 8):
                    temp = p.prettify()
                    index = temp.find('<div class="comments"')
                    temp = temp[:index]

                    # add to dict as a key, val = time passed

                    tp = num

                    if t == 'hours':
                        tp += 10
                    elif t == 'days':
                        tp += 20


                    posts[temp] = tp
                else:
                    run = False
                    break

            print('after soup')
  

    print('Total posts last week: ' + str(len(posts)))
    SaveNames(fn, posts)
    wd.quit()

def SaveNames(fileName, posts):
    print('Saving to ' + fileName + '...')
    file = open(fileName, 'w')
    for p in sorted(posts, key=posts.get):
        try:
            file.write(p + '\n\n\n\n\n\n\n\n')
        except:
            pass

    print('File Saved!')
    file.close()
        


GetPosts()
