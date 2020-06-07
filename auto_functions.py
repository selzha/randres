#===================================================================

# Useful functions for autocompletion of apps

#===================================================================

import time
import re
import string
import datetime as dt
from dateutil import relativedelta
import numpy as np

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

#===================================================================
# Example Inputs and Useful Objects
#===================================================================

details_example = {'id': 9900,
 'user_id': 99,
 'job_id': 999,
 'role_id': 999,
 'firstname': 'Michael',
 'lastname': 'Sanderson',
 'gender': 'Male',
 'race': 'Black',
 'dob': '3/13/1973',
 'phone': 1234561234,
 'email': 'tuzmw973@mt2015.com',
 'addy': "213 Delware Avenue",
 'addy_city': 'SHREVEPORT',
 'addy_state': 'LA',
 'addy_zip': 71115,
 'start_date': '2019-11-05',
 'schl_name': 'HELEN COX HIGH SCHOOL',
 'schl_addy': '2200 LAPALCO BLVD HARVEY',
 'schl_state': 'LA',
 'schl_city': 'SHREVEPORT',
 'schl_zip': 70058,
 'grad_year': 1991,
 'col_name': 'Central Louisiana Technical Community College',
 'col_addy': '4311 South MacArthur Drive',
 'col_state': 'LA',
 'col_zip': 71302,
 'bachelors': 0,
 'major': 'Legal Office Support',
 'social': 529316230,
 'whywork': 'I want to use and improve my skills. ',
 'firm': 'TESTING',
 'city': 'Bossier City',
 'state': 'LA',
 'street': '3836 Industrial Circle  ',
 'zipcode': 71112,
 'jobtitle': 'Test',
 'link': '',
 'raw_name': 'TESTING',
 'hist': [{'id': 17410,
   'name': 'Sf Spice',
   'position': 'Cook',
   'addy': '1640 Tide Ct',
   'city': 'WOODLAND',
   'state': 'CA',
   'zip': 95776,
   'supervisor': 'Nico Richards',
   'start': '7/2018',
   'end': 'Present',
   'whyleave': '',
   'phone': '(530) 736-7909',
   'type': 'Spices',
   'sic': 54,
   'duties': ['Operate dish washer per approved guidelines.',
    'Performed basic cleaning tasks as needed or directed by supervisor',
    'Stocked cooler with food needed for that day']},
  {'id': 17411,
   'name': 'Las Islitas Ostioneria',
   'position': 'Dishwasher',
   'addy': '737 East St',
   'city': 'WOODLAND',
   'state': 'CA',
   'zip': 95776,
   'supervisor': 'Cullen George',
   'start': '8/2017',
   'end': '7/2018',
   'whyleave': 'Ready to try new things.',
   'phone': '(530) 005-7951',
   'type': 'Restaurants',
   'sic': 58,
   'duties': ['Cleaned and set up chef case with prepared foods.',
    'Maintain all cleaning/washing equipment at proper temperature and in proper']},
  {'id': 17412,
   'name': 'Famous Footwear',
   'position': 'Customer Service Associate',
   'addy': '2145 Bronze Star Dr # 400',
   'city': 'WOODLAND',
   'state': 'CA',
   'zip': 95776,
   'supervisor': 'Kole Warren',
   'start': '11/2016',
   'end': '8/2017',
   'whyleave': 'Looking for promotion opportunities.',
   'phone': '(530) 330-4620',
   'type': 'Shoes-retail',
   'sic': 56,
   'duties': ['Answer questions regarding the store and its merchandise.',
    'Performed countdown of money at shift beginning and end']}]}

details_example_2 = {'id': 1330,
 'user_id': 45,
 'job_id': 221,
 'role_id': 221,
 'firstname': 'Samantha',
 'lastname': 'Andrews',
 'gender': 'Female',
 'race': 'White',
 'dob': '9/17/1988',
 'phone': 4293821036,
 'email': 'qieza318@mt2015.com',
 'addy': "2020 Oxford st",
 'addy_city': 'Berkeley',
 'addy_state': 'CA',
 'addy_zip': 94709,
 'start_date': '2019-11-05',
 'schl_name': 'HELEN COX HIGH SCHOOL',
 'schl_addy': '2200 LAPALCO BLVD HARVEY',
 'schl_state': 'LA',
 'schl_city': 'SHREVEPORT',
 'schl_zip': 70058,
 'grad_year': 1991,
 'col_name': 'Central Louisiana Technical Community College',
 'col_addy': '4311 South MacArthur Drive',
 'col_state': 'LA',
 'col_zip': 71302,
 'bachelors': 0,
 'major': 'Legal Office Support',
 'social': 526078545,
 'whywork': 'I want to use and improve my skills. ',
 'firm': 'TESTING',
 'city': 'Bossier City',
 'state': 'LA',
 'street': '3836 Industrial Circle  ',
 'zipcode': 71112,
 'jobtitle': 'Test',
 'link': '',
 'raw_name': 'TESTING',
 'hist': [{'id': 3299,
   'name': 'Witts Powder Coating',
   'position': 'Handler',
   'addy': '1328 Driftwood Dr',
   'city': 'BOSSIER CITY',
   'state': 'LA',
   'zip': 71111,
   'supervisor': 'Armani Russell',
   'start': '12/2017',
   'end': 'Present',
   'whyleave': '',
   'phone': '(318) 134-7492',
   'type': 'Powder Coatings (mfrs)',
   'duties': ['Responsible for physically loading and unloading packages',
    'Transported material by use of forklifts, pallet jacks and hand trucks.',
    'Lift, carry, push and pull packages as required']},
  {'id': 3300,
   'name': 'Martins Alternators & Starters',
   'position': 'Delivery Driver / Courier',
   'addy': '2214 Barksdale Blvd',
   'city': 'BOSSIER CITY',
   'state': 'LA',
   'zip': 71112,
   'supervisor': 'Jamarcus Powell',
   'start': '5/2016',
   'end': '12/2017',
   'whyleave': 'I was exploring new lines of work.',
   'phone': '(318) 570-9737',
   'type': 'Alternators & Starters-marine (mfrs)',
   'duties': ['Place orders for biweekly or weekly deliveries',
    'Perform vehicle safety checks before departure.',
    'Check with dispatcher after completed deliveries, in order to confirm deliveries and collections and to receive instructions for other deliveries.']},
  {'id': 3301,
   'name': 'Neff Rental',
   'position': 'Handler',
   'addy': '3836 Industrial Cir',
   'city': 'BOSSIER CITY',
   'state': 'LA',
   'zip': 71112,
   'supervisor': 'Darian Payne',
   'start': '6/2014',
   'end': '5/2016',
   'whyleave': 'Looking for promotion opportunities.',
   'phone': '(318) 226-6551',
   'type': 'Construction-building Contractors',
   'duties': ['Sorted packages by hands in an efficient manner.',
    'Stack materials in accordance to instructions']}]}

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

# Possible SIC does and positions used for jobs in each.
# SIC Code Reference: https://mckimmoncenter.ncsu.edu/2digitsiccodes/
fast_food_positions   = ['Crew Member', 'Cashier', 'Food prep / service', 'Cook']
food_positions        = ['Server', 'Dishwasher', 'Cashier', 'Host', 'Cook']
office_positions      = ['Office manager', 'Receptionist', 'Assistant']
hospitality_positions = ['Housekeeper','Receptionist']
delivery_positions    = ['Package Handler', 'Handler', 'Laborer',
                        'Delivery Driver / Courier', 'Dockworker', 'Warehouse Associate']
standard_positions    = ['Team Member', 'Retail Associate', 'Cashier',
                        'Stocker', 'Customer Service Associate'] # Works for all but food

pos_map = { 15: office_positions,
            24: office_positions,
            25: office_positions,
            34: office_positions,
            36: office_positions,
            42: office_positions,
            53: standard_positions,
            54: fast_food_positions,
            56: standard_positions,
            58: food_positions,
            64: office_positions,
            65: office_positions,
            70: hospitality_positions + food_positions,
            73: office_positions,
            80: office_positions,}

# common names
common_first_names = ['Jacob','Emily','Michael','Hannah','Matthew','Madison','Joshua','Ashley','Christopher','Sarah','Nicholas','Alexis','Andrew','Samantha','Joseph','Jessica','Daniel','Elizabeth','Tyler','Taylor','William','Lauren','Brandon','Alyssa','Ryan','Kayla','John','Abigail','Zachary','Brianna','David','Olivia','Anthony','Emma','James','Megan','Justin','Grace','Alexander','Victoria','Jonathan','Rachel','Christian','Anna','Austin','Sydney','Dylan','Destiny','Ethan','Morgan','Benjamin','Jennifer','Noah','Jasmine','Samuel','Haley','Robert','Julia','Nathan','Kaitlyn','Cameron','Nicole','Kevin','Amanda','Thomas','Katherine','Jose','Natalie','Hunter','Hailey','Jordan','Alexandra','Kyle','Savannah','Caleb','Chloe','Jason','Rebecca','Logan','Stephanie','Aaron','Maria','Eric','Sophia','Brian','Mackenzie','Gabriel','Allison','Adam','Isabella','Jack','Mary','Isaiah','Amber','Juan','Danielle','Luis','Gabrielle','Connor','Jordan','Charles','Brooke','Elijah','Michelle','Isaac','Sierra','Steven','Katelyn','Evan','Andrea','Jared','Madeline','Sean','Sara','Timothy','Kimberly','Luke','Courtney','Cody','Erin','Nathaniel','Brittany','Alex','Vanessa','Seth','Jenna','Mason','Jacqueline','Richard','Caroline','Carlos','Faith','Angel','Makayla','Patrick','Bailey','Devin','Paige','Bryan','Shelby','Cole','Melissa','Jackson','Kaylee','Ian','Christina','Garrett','Trinity','Trevor','Mariah','Jesus','Caitlin','Chase','Autumn','Adrian','Marissa','Mark','Angela','Blake','Breanna','Sebastian','Catherine','Antonio','Zoe','Lucas','Briana','Jeremy','Jada','Gavin','Laura','Miguel','Claire','Julian','Alexa','Dakota','Kelsey','Alejandro','Kathryn','Jesse','Leslie','Dalton','Alexandria','Bryce','Sabrina','Tanner','Mia','Kenneth','Isabel','Stephen','Molly','Jake','Katie','Victor','Leah','Spencer','Gabriella','Marcus','Cheyenne','Paul','Cassandra','Brendan','Tiffany','Jeremiah','Erica','Xavier','Lindsey','Jeffrey','Kylie','Tristan','Amy','Jalen','Diana','Jorge','Cassidy','Edward','Mikayla','Riley','Ariana','Colton','Margaret','Wyatt','Kelly','Joel','Miranda','Maxwell','Maya','Aidan','Melanie','Travis','Audrey','Shane','Jade','Colin','Gabriela','Dominic','Caitlyn','Carson','Angel','Vincent','Jillian','Derek','Alicia','Oscar','Jocelyn','Grant','Erika','Eduardo','Lily','Peter','Heather','Henry','Madelyn','Parker','Adriana','Collin','Arianna','Hayden','Lillian','George','Kiara','Bradley','Riley','Mitchell','Crystal','Devon','Mckenzie','Ricardo','Meghan','Shawn','Skylar','Taylor','Ana','Nicolas','Britney','Gregory','Angelica','Francisco','Kennedy','Liam','Chelsea','Kaleb','Daisy','Preston','Kristen','Erik','Veronica','Alexis','Isabelle','Owen','Summer','Omar','Hope','Diego','Brittney','Dustin','Lydia','Corey','Hayley','Fernando','Evelyn','Clayton','Bethany','Carter','Shannon','Ivan','Karen','Jaden','Michaela','Javier','Jamie','Alec','Daniela','Johnathan','Angelina','Scott','Kaitlin','Manuel','Karina','Cristian','Sophie','Alan','Sofia','Raymond','Diamond','Brett','Payton','Max','Cynthia','Andres','Alexia','Gage','Valerie','Mario','Monica','Dawson','Peyton','Dillon','Carly','Cesar','Bianca','Wesley','Hanna','Levi','Brenda','Jakob','Rebekah','Chandler','Alejandra','Martin','Mya','Malik','Avery','Edgar','Brooklyn','Sergio','Ashlyn','Trenton','Lindsay','Josiah','Ava','Nolan','Desiree','Marco','Alondra','Peyton','Camryn','Harrison','Ariel','Hector','Naomi','Micah','Jordyn','Roberto','Kendra','Drew','Mckenna','Brady','Holly','Erick','Julie','Conner','Kendall','Jonah','Kara','Casey','Jasmin','Jayden','Selena','Edwin','Esmeralda','Emmanuel','Amaya','Andre','Kylee','Phillip','Maggie','Brayden','Makenzie','Landon','Claudia','Giovanni','Kyra','Bailey','Cameron','Ronald','Karla','Braden','Kathleen','Damian','Abby','Donovan','Delaney','Ruben','Amelia','Frank','Casey','Gerardo','Serena','Pedro','Savanna','Andy','Aaliyah','Chance','Giselle','Abraham','Mallory','Calvin','April','Trey','Adrianna','Cade','Raven','Donald','Christine','Derrick','Kristina','Payton','Nina','Darius','Asia','Enrique','Natalia','Keith','Valeria','Raul','Aubrey','Jaylen','Lauryn','Troy','Kate','Jonathon','Patricia','Cory','Jazmin','Marc','Rachael','Eli','Katelynn','Skyler','Cierra','Rafael','Alison','Trent','Nancy','Griffin','Macy','Colby','Elena','Johnny','Kyla','Chad','Katrina','Armando','Jazmine','Kobe','Joanna','Caden','Tara','Marcos','Gianna','Cooper','Juliana','Elias','Fatima','Brenden','Sadie','Israel','Allyson','Avery','Gracie','Zane','Guadalupe','Dante','Genesis','Josue','Yesenia','Zackary','Julianna','Allen','Skyler','Mathew','Tatiana','Dennis','Alexus','Leonardo','Alana','Ashton','Elise','Philip','Kirsten','Julio','Nadia','Miles','Sandra','Damien','Ruby','Ty','Dominique','Gustavo','Haylee','Drake','Jayla','Jaime','Tori','Simon','Cindy','Jerry','Ella','Curtis','Sidney','Kameron','Tessa','Lance','Carolina','Brock','Jaqueline','Bryson','Camille','Alberto','Carmen','Dominick','Whitney','Jimmy','Vivian','Kaden','Priscilla','Douglas','Bridget','Gary','Celeste','Brennan','Kiana','Zachery','Makenna','Randy','Alissa','Louis','Madeleine','Larry','Miriam','Nickolas','Natasha','Albert','Ciara','Tony','Cecilia','Fabian','Kassandra','Keegan','Mercedes','Saul','Reagan','Danny','Aliyah','Tucker','Josephine','Myles','Charlotte','Damon','Rylee','Arturo','Shania','Corbin','Kira','Deandre','Meredith','Ricky','Eva','Kristopher','Lisa','Lane','Dakota','Pablo','Hallie','Darren','Anne','Jarrett','Rose','Zion','Liliana','Alfredo','Kristin','Micheal','Deanna','Angelo','Imani','Carl','Marisa','Oliver','Kailey','Kyler','Annie','Tommy','Nia','Walter','Carolyn','Dallas','Anastasia','Jace','Brenna','Quinn','Dana','Theodore','Shayla','Grayson','Ashlee','Lorenzo','Kassidy','Joe','Alaina','Arthur','Wendy','Bryant','Rosa','Roman','Logan','Brent','Tabitha','Russell','Paola','Ramon','Callie','Lawrence','Addison','Moises','Lucy','Aiden','Gillian','Quentin','Clarissa','Jay','Esther','Tyrese','Destinee','Tristen','Josie','Emanuel','Denise','Salvador','Katlyn','Terry','Mariana','Morgan','Bryanna','Jeffery','Emilee','Esteban','Georgia','Tyson','Kamryn','Braxton','Deja','Branden','Ashleigh','Marvin','Cristina','Brody','Ruth','Craig','Baylee','Ismael','Heaven','Rodney','Raquel','Isiah','Monique','Marshall','Teresa','Maurice','Helen','Ernesto','Krystal','Emilio','Tiana','Brendon','Cassie','Kody','Kayleigh','Eddie','Marina','Malachi','Ivy','Abel','Heidi','Keaton','Clara','Jon','Ashton','Shaun','Meagan','Skylar','Gina','Ezekiel','Linda','Nikolas','Gloria','Santiago','Jacquelyn','Kendall','Ellie','Axel','Jenny','Camden','Renee','Trevon','Daniella','Bobby','Lizbeth','Conor','Anahi','Jamal','Virginia','Lukas','Gisselle','Malcolm','Kaitlynn','Zackery','Julissa','Jayson','Cheyanne','Javon','Lacey','Roger','Haleigh','Reginald','Marie','Zachariah','Martha','Desmond','Eleanor','Felix','Kierra','Johnathon','Tiara','Dean','Talia','Quinton','Eliza','Ali','Kaylie','Davis','Mikaela','Gerald','Harley','Rodrigo','Jaden','Demetrius','Hailee','Billy','Madalyn','Rene','Kasey','Reece','Ashlynn','Kelvin','Brandi','Leo','Lesly','Justice','Elisabeth','Chris','Allie','Guillermo','Viviana','Kevon','Cara','Steve','Marisol','Frederick','India','Clay','Litzy','Weston','Tatyana','Dorian','Melody','Hugo','Jessie','Roy','Brandy','Orlando','Alisha','Terrance','Hunter','Kai','Noelle','Khalil','Carla','Graham','Francesca','Noel','Tia','Willie','Layla','Nathanael','Krista','Terrell','Zoey','Tyrone','Carley','Camron','Janet','Mauricio','Carissa','Amir','Iris','Nelson','Susan','Darian','Kaleigh','Jarod','Tyler','Kade','Tamara','Reese','Theresa','Kristian','Yasmine','Garret','Tatum','Rodolfo','Sharon','Marquis','Alice','Dane','Yasmin','Felipe','Tamia','Todd','Abbey','Elian','Alayna','Walker','Kali','Mateo','Lilly','Jaylon','Bailee','Kenny','Lesley','Ezra','Mckayla','Bruce','Ayanna','Damion','Serenity','Ross','Karissa','Francis','Precious','Tate','Jane','Reid','Maddison','Warren','Jayda','Byron','Lexi','Randall','Kelsie','Bennett','Phoebe','Jermaine','Halle','Triston','Kiersten','Harley','Kiera','Jaquan','Tyra','Jessie','Annika','Duncan','Felicity','Franklin','Taryn','Reed','Kaylin','Charlie','Ellen','Blaine','Kiley','Braeden','Jaclyn','Holden','Rhiannon','Ahmad','Madisyn','Issac','Colleen','Melvin','Joy','Moses','Charity','Kendrick','Pamela','Sawyer','Tania','Solomon','Fiona','Sam','Kaila','Alvin','Irene','Cedric','Alyson','Jaylin','Annabelle','Jordon','Emely','Mohammad','Angelique','Beau','Alina','Elliot','Johanna','Lee','Regan','Darrell','Janelle','Jarred','Janae','Mohamed','Madyson','Davion','Paris','Wade','Justine','Tomas','Chelsey','Uriel','Sasha','Jaxon','Paulina','Deven','Mayra','Maximilian','Zaria','Gilberto','Skye','Rogelio','Cora','Ronnie','Brisa','Julius','Emilie','Allan','Felicia','Joey','Tianna','Brayan','Larissa','Deshawn','Macie','Terrence','Aurora','Noe','Sage','Alfonso','Lucia','Ahmed','Alma','Tyree','Chasity','Tyrell','Ann','Jerome','Deborah','Devan','Nichole','Neil','Jayden','Ramiro','Alanna','Pierce','Malia','Davon','Carlie','Devonte','Angie','Leon','Nora','Jamie','Sylvia','Adan','Carrie','Eugene','Kailee','Stanley','Elaina','Wayne','Sonia','Marlon','Barbara','Leonard','Kenya','Quincy','Genevieve','Will','Piper','Alvaro','Marilyn','Ernest','Amari','Harry','Macey','Jonas','Marlene','Addison','Julianne','Ray','Tayler','Alonzo','Brooklynn','Jadon','Lorena','Keyshawn','Perla','Rolando','Elisa','Mohammed','Eden','Tristin','Kaley','Donte','Leilani','Leonel','Miracle','Dominique','Devin','Wilson','Aileen','Gilbert','Chyna','Kieran','Esperanza','Coby','Athena','Dangelo','Regina','Colten','Adrienne','Keenan','Shyanne','Koby','Luz','Jarrod','Tierra','Dale','Clare','Toby','Cristal','Dwayne','Eliana','Harold','Kelli','Elliott','Eve','Osvaldo','Sydnee','Cyrus','Madelynn','Kolby','Breana','Sage','Melina','Coleman','Arielle','Declan','Justice','Adolfo','Toni','Ariel','Corinne','Brennen','Abbigail','Darryl','Maia','Trace','Tess','Efrain','Ciera','Orion','Ebony','Rudy','Lena','Shamar','Maritza','Keshawn','Lexie','Ulises','Isis','Darien','Aimee','Braydon','Leticia','Ben','Sydni','Vicente','Sarai','Nasir','Halie','Dayton','Alivia','Joaquin','Destiney','Karl','Laurel','Dandre','Edith','Isaias','Fernanda','Cullen','Carina','Rylan','Amya','Sterling','Destini','Quintin','Aspen','Stefan','Nathalie','Brice','Paula','Lewis','Tanya','Gunnar','Tina','Humberto','Frances','Alfred','Christian','Nigel','Elaine','Asher','Shayna','Agustin','Aniya','Daquan','Mollie','Easton','Ryan','Salvatore','Essence','Jaron','Simone','Nathanial','Kyleigh','Ralph','Nikki','Everett','Anya','Tobias','Reyna','Hudson','Savanah','Marquise','Kaylyn','Glenn','Nicolette','Antoine','Abbie','Jasper','Montana','Elvis','Kailyn','Kane','Itzel','Sidney','Leila','Aron','Cayla','Ezequiel','Stacy','Tylor','Robin','Dashawn','Araceli','Devyn','Candace','Mike','Dulce','Silas','Noemi','Jaiden','Aleah','Jayce','Jewel','Deonte','Ally','Romeo','Mara','Deon','Nayeli','Cristopher','Karlee','Freddy','Keely','Kurt','Micaela','Kolton','Alisa','River','Desirae','August','Leanna','Clarence','Antonia','Roderick','Judith','Derick','Brynn','Jamar','Jaelyn','Raphael','Raegan','Kareem','Katelin','Muhammad','Sienna','Rohan','Celia','Demarcus','Yvette','Sheldon','Juliet','Cayden','Anika','Markus','Emilia','Luca','Calista','Tre','Carlee','Jean','Eileen','Titus','Kianna','Jamison','Thalia','Rory','Rylie','Brad','Rosemary','Clinton','Daphne','Jaylan','Kacie','Emiliano','Karli','Jevon','Micah','Julien','Ericka','Lamar','Jadyn','Alonso','Lyndsey','Cordell','Hana','Gordon','Haylie','Ignacio','Madilyn','Cruz','Blanca','Jett','Laila','Keon','Kayley','Baby','Katarina','Rashad','Kellie','Tariq','Maribel','Armani','Sandy','Milton','Joselyn','Deangelo','Kaelyn','Geoffrey','Kathy','Elisha','Madisen','Moshe','Carson','Asa','Margarita','Bernard','Stella','Bret','Juliette','Darion','Devon','Darnell','Bria','Izaiah','Camila','Irvin','Donna','Jairo','Helena','Howard','Lea','Aldo','Jazlyn','Norman','Jazmyn','Zechariah','Skyla','Ayden','Christy','Garrison','Joyce','Stuart','Katharine','Travon','Karlie','Kellen','Lexus','Shemar','Alessandra','Dillan','Salma','Junior','Delilah','Darrius','Moriah','Rhett','Beatriz','Barry','Celine','Kamron','Lizeth','Jude','Brianne','Rigoberto','Kourtney','Amari','Sydnie','Jovan','Mariam','Perry','Stacey','Octavio','Robyn','Kole','Hayden','Misael','Janessa','Hassan','Kenzie','Jaren','Jalyn','Latrell','Sheila','Roland','Meaghan','Quinten','Aisha','German','Shawna','Ibrahim','Jaida','Justus','Estrella','Gonzalo','Marley','Nehemiah','Melinda','Forrest','Ayana','Mackenzie','Karly','Talon','Devyn','Anton','Nataly','Chaz','Loren','Leroy','Rosalinda','Guadalupe','Brielle','Winston','Laney','Antwan','Sally','Austen','Lizette','Brooks','Tracy','Conrad','Lilian','Greyson','Rebeca','Dion','Chandler','Lincoln','Jenifer','Earl','Diane','Jaydon','Valentina','Landen','America','Gunner','Candice','Brenton','Abigayle','Jefferson','Susana','Fredrick','Aliya','Kurtis','Casandra','Maximillian','Harmony','Stephan','Jacey','Stone','Alena','Shannon','Aylin','Shayne','Carol','Stephon','Shea','Karson','Stephany','Nestor','Aniyah','Tristian','Zoie','Frankie','Jackeline','Gianni','Alia','Keagan','Gwendolyn','Dimitri','Savana','Kory','Damaris','Zakary','Violet','Daryl','Marian','Donavan','Anita','Draven','Jaime','Jameson','Alexandrea','Clifton','Dorothy','Emmett','Jaiden','Cortez','Kristine','Destin','Carli','Jamari','Gretchen','Dallin','Janice','Estevan','Annette','Grady','Mariela','Davin','Amani','Santos','Maura','Marcel','Bella','Carlton','Kaylynn','Dylon','Lila','Mitchel','Armani','Clifford','Anissa','Syed','Aubree','Dexter','Kelsi','Adonis','Greta','Keyon','Kaya','Reynaldo','Kayli','Devante','Lillie','Arnold','Willow','Clark','Ansley','Kasey','Catalina','Sammy','Lia','Thaddeus','Maci','Glen','Mattie','Jarvis','Celina','Nick','Shyann','Ulysses','Alysa','Garett','Jaquelin','Infant','Quinn','Keanu','Cecelia','Kenyon','Kallie','Dwight','Kasandra','Kent','Chaya','Denzel','Hailie','Lamont','Haven','Houston','Maegan','Layne','Maeve','Darin','Rocio','Jorden','Yolanda','Anderson','Christa','Kayden','Gabriel','Khalid','Kari','Antony','Noelia','Deondre','Jeanette','Ellis','Kaylah','Marquez','Marianna','Ari','Nya','Cornelius','Kennedi','Reuben','Presley','Austyn','Yadira','Brycen','Elissa','Abram','Nyah','Remington','Shaina','Braedon','Reilly','Hamza','Alize','Ryder','Amara','Zaire','Arlene','Terence','Izabella','Guy','Lyric','Jamel','Aiyana','Kelly','Allyssa','Porter','Drew','Tevin','Rachelle','Alexandro','Adeline','Dario','Jacklyn','Jordy','Jesse','Trever','Citlalli','Jackie','Giovanna','Judah','Liana','Keven','Brook','Raymundo','Graciela','Cristobal','Princess','Josef','Selina','Paris','Chanel','Colt','Elyse','Giancarlo','Cali','Rahul','Berenice','Savion','Iliana','Deshaun','Jolie','Josh','Annalise','Korey','Caitlynn','Gerard','Christiana','Jacoby','Sarina','Lonnie','Cortney','Reilly','Darlene','Seamus','Dasia','Don','London','Giovanny','Yvonne','Jamil','Karley','Kristofer','Shaylee','Samir','Kristy','Vernon','Myah','Benny','Ryleigh','Dominik','Amira','Finn','Juanita','Jan','Dariana','Kaiden','Teagan','Cale','Kiarra','Irving','Ryann','Jaxson','Yamilet','Marcelo','Sheridan','Nico','Alexys','Rashawn','Baby','Aubrey','Kacey','Gaven','Shakira','Jabari','Dianna','Sincere','Lara','Kirk','Isabela','Maximus','Reina','Mikel','Shirley','Davonte','Jaycee','Elmer','Silvia','Heath','Tatianna','Justyn','Eryn','Kadin','Ingrid','Alden','Keara','Kelton','Randi','Brandan','Reanna','Courtney','Kalyn','Camren','Lisette','Dewayne','Monserrat','Duane','Abril','Maverick','Ivana','Darrin','Lori','Darrion','Darby','Nikhil','Kaela','Sonny','Maranda','Abdullah','Parker','Chaim','Darian','Nathen','Jasmyn','Xzavier','Jaylin','Bronson','Katia','Efren','Ayla','Jovani','Bridgette','Phoenix','Elyssa','Reagan','Hillary','Aden','Kinsey','Blaze','Yazmin','Gideon','Caleigh','Luciano','Rita','Royce','Asha','Tyrek','Dayana','Tyshawn','Nikita','Deontae','Chantel','Fidel','Reese','Gaige','Stefanie','Neal','Nadine','Ronaldo','Samara','Matteo','Unique','Prince','Michele','Rickey','Sonya','Deion','Hazel','Denver','Patience','Benito','Cielo','London','Mireya','Samson','Paloma','Bernardo','Aryanna','Raven','Magdalena','Simeon','Anaya','Turner','Dallas','Carlo','Joelle','Gino','Norma','Johan','Arely','Rocky','Kaia','Ryley','Misty','Domenic','Taya','Hugh','Deasia','Trystan','Trisha','Emerson','Elsa','Joan','Joana','Trevion','Alysha','Heriberto','Aracely','Marques','Bryana','Raheem','Dawn','Tyreek','Alex','Vaughn','Brionna','Clint','Katerina','Nash','Ali','Mariano','Bonnie','Myron','Hadley','Ladarius','Martina','Lloyd','Maryam','Omari','Jazmyne','Pierre','Shaniya','Keshaun','Alycia','Rick','Dejah','Xander','Emmalee','Amos','Estefania','Eliseo','Jakayla','Jeff','Lilliana','Bradly','Nyasia','Freddie','Anjali','Kavon','Daisha','Mekhi','Myra','Sabastian','Amiya','Shea','Belen','Dan','Jana','Adrien','Aja','Alessandro','Saige','Blaise','Annabel','Isai','Scarlett','Kian','Destany','Maximiliano','Joanne','Paxton','Aliza','Rasheed','Ashly','Brodie','Cydney','Donnie','Fabiola','Isidro','Gia','Jaeden','Keira','Javion','Roxanne','Jimmie','Kaci','Johnnie','Abigale','Kennedy','Abagail','Tyrique','Janiya','Andreas','Odalys','Augustus','Aria','Jalon','Daija','Jamir','Delia','Valentin','Kameron','Korbin','Raina','Lawson','Ashtyn','Maxim','Dayna','Fred','Katy','Herbert','Lourdes','Bruno','Emerald','Donavon','Kirstin','Javonte','Marlee','Ean','Neha','Kamren','Beatrice','Rowan','Blair','Alek','Kori','Brandyn','Luisa','Demarco','Yasmeen','Harvey','Annamarie','Hernan','Breonna','Alexzander','Jena','Bo','Leann','Branson','Rhianna','Brennon','Yessenia','Genaro','Breanne','Jamarcus','Katlynn','Aric','Laisha','Barrett','Mandy','Rey','Amina','Braiden','Jailyn','Brant','Jayde','Dontae','Jill','Jovany','Kaylan','Kale','Kenna','Nicklaus','Antoinette','Zander','Rayna','Dillion','Sky','Donnell','Iyana','Kylan','Keeley','Treyvon','Kenia','Vincenzo','Maiya','Dayne','Melisa','Francesco','Adrian','Isaak','Marlen']
common_last_names = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez','Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin','Lee','Perez','Thompson','White','Harris','Sanchez','Clark','Ramirez','Lewis','Robinson','Walker','Young','Allen','King','Wright','Scott','Torres','Nguyen','Hill','Flores','Green','Adams','Nelson','Baker','Hall','Rivera','Campbell','Mitchell','Carter','Roberts','Gomez','Phillips','Evans','Turner','Diaz','Parker','Cruz','Edwards','Collins','Reyes','Stewart','Morris','Morales','Murphy','Cook','Rogers','Gutierrez','Ortiz','Morgan','Cooper','Peterson','Bailey','Reed','Kelly','Howard','Ramos','Kim','Cox','Ward','Richardson','Watson','Brooks','Chavez','Wood','James','Bennett','Gray','Mendoza','Ruiz','Hughes','Price','Alvarez','Castillo','Sanders','Patel','Myers','Long','Ross','Foster','Jimenez','Powell','Jenkins','Perry','Russell','Sullivan','Bell','Coleman','Butler','Henderson','Barnes','Gonzales','Fisher','Vasquez','Simmons','Romero','Jordan','Patterson','Alexander','Hamilton','Graham','Reynolds','Griffin','Wallace','Moreno','West','Cole','Hayes','Bryant','Herrera','Gibson','Ellis','Tran','Medina','Aguilar','Stevens','Murray','Ford','Castro','Marshall','Owens','Harrison','Fernandez','Mcdonald','Woods','Washington','Kennedy','Wells','Vargas','Henry','Chen','Freeman','Webb','Tucker','Guzman','Burns','Crawford','Olson','Simpson','Porter','Hunter','Gordon','Mendez','Silva','Shaw','Snyder','Mason','Dixon','Munoz','Hunt','Hicks','Holmes','Palmer','Wagner','Black','Robertson','Boyd','Rose','Stone','Salazar','Fox','Warren','Mills','Meyer','Rice','Schmidt','Garza','Daniels','Ferguson','Nichols','Stephens','Soto','Weaver','Ryan','Gardner','Payne','Grant','Dunn','Kelley','Spencer','Hawkins','Arnold','Pierce','Vazquez','Hansen','Peters','Santos','Hart','Bradley','Knight','Elliott','Cunningham','Duncan','Armstrong','Hudson','Carroll','Lane','Riley','Andrews','Alvarado','Ray','Delgado','Berry','Perkins','Hoffman','Johnston','Matthews','Pena','Richards','Contreras','Willis','Carpenter','Lawrence','Sandoval','Guerrero','George','Chapman','Rios','Estrada','Ortega','Watkins','Greene','Nunez','Wheeler','Valdez','Harper','Burke','Larson','Santiago','Maldonado','Morrison']
common_male_first_names = ['James','John','Robert','Michael','William','David','Richard','Joseph','Thomas','Charles','Christopher','Daniel','Matthew','Anthony','Donald','Mark','Paul','Steven','Andrew','Kenneth','Joshua','George','Kevin','Brian','Edward','Ronald','Timothy','Jason','Jeffrey','Ryan','Jacob','Gary','Nicholas','Eric','Stephen','Jonathan','Larry','Justin','Scott','Brandon','Frank','Benjamin','Gregory','Samuel','Raymond','Patrick','Alexander','Jack','Dennis','Jerry','Tyler','Aaron','Jose','Henry','Douglas','Adam','Peter','Nathan','Zachary','Walter','Kyle','Harold','Carl','Jeremy','Keith','Roger','Gerald','Ethan','Arthur','Terry','Christian','Sean','Lawrence','Austin','Joe','Noah','Jesse','Albert','Bryan','Billy','Bruce','Willie','Jordan','Dylan','Alan','Ralph','Gabriel','Roy','Juan','Wayne','Eugene','Logan','Randy','Louis','Russell','Vincent','Philip','Bobby','Johnny','Bradley']
common_female_first_name = ['Mary','Patricia','Jennifer','Linda','Elizabeth','Barbara','Susan','Jessica','Sarah','Karen','Nancy','Margaret','Lisa','Betty','Dorothy','Sandra','Ashley','Kimberly','Donna','Emily','Michelle','Carol','Amanda','Melissa','Deborah','Stephanie','Rebecca','Laura','Sharon','Cynthia','Kathleen','Helen','Amy','Shirley','Angela','Anna','Brenda','Pamela','Nicole','Ruth','Katherine','Samantha','Christine','Emma','Catherine','Debra','Virginia','Rachel','Carolyn','Janet','Maria','Heather','Diane','Julie','Joyce','Victoria','Kelly','Christina','Joan','Evelyn','Lauren','Judith','Olivia','Frances','Martha','Cheryl','Megan','Andrea','Hannah','Jacqueline','Ann','Jean','Alice','Kathryn','Gloria','Teresa','Doris','Sara','Janice','Julia','Marie','Madison','Grace','Judy','Theresa','Beverly','Denise','Marilyn','Amber','Danielle','Abigail','Brittany','Rose','Diana','Natalie','Sophia','Alexis','Lori','Kayla','Jane']

def generate_fake_phone_number(formatted=True):
    try:
        n = '0000000000'
        while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
            n = str(np.random.randint(10**9, 10**10-1))
        n = code + n[3:]
    except:
        n = '0000000000'
        while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
            n = str(np.random.randint(10**9, 10**10-1))
    if formatted:
        return '(' + n[:3] + ') ' + n[3:6] + '-' + n[6:]
    else:
        return n

#===================================================================
# Useful Functions for Robots
#===================================================================

def calculate_experience(details, pos_list = [], sic_list = [], both_required = True):

    # If no list is provided for positions or SIC codes, consider all possible values
    if len(pos_list) == 0:
        pos_list = ['Crew Member', 'Cashier', 'Food prep / service', 'Cook', 'Server',
                    'Dishwasher', 'Host', 'Office manager', 'Receptionist', 'Assistant',
                    'Housekeeper', 'Package Handler', 'Handler', 'Laborer',
                    'Delivery Driver / Courier', 'Dockworker', 'Warehouse Associate',
                    'Team Member', 'Retail Associate','Stocker', 'Customer Service Associate']

    if len(sic_list) == 0:
        sic_list = [15, 24, 25, 34, 36, 42, 53, 54, 56, 58, 64, 65, 70, 73, 80]


    # Extract start/end dates for past jobs meeting desired job criteria list
    list_dates = []

    for h in details['hist']:

        pos_correct = h['position'] in pos_list
        sic_correct = h['sic']      in sic_list

        if   (both_required == True):  include = pos_correct and sic_correct
        elif (both_required == False): include = pos_correct or  sic_correct

        if (include == True): list_dates.append( [  h['start'], h['end']  ] )


    # Calculate experience in months ( date[0] = Start date, date[1] = End date )
    for date in list_dates:

        if (date[1] == 'Present'):
            mon  = dt.datetime.now().month
            year = dt.datetime.now().year
            date[1] = str(mon) + '/' + str(year)

        st_mon, st_year = date[0].split('/')
        ed_mon, ed_year = date[1].split('/')

        st_date = dt.date( year = int(st_year), month = int(st_mon), day = 1 )
        ed_date = dt.date( year = int(ed_year), month = int(ed_mon), day = 1 )

        delta = relativedelta.relativedelta(ed_date, st_date)
        duration_months = (delta.years * 12) + delta.months

        date.append(duration_months)

    exper_months = sum( [date[2] for date in list_dates] )

    return exper_months

def str_format(x):
    try:
        words = re.findall("[\w']+", x)
        new_words = [w.capitalize() if not (w.lower() == 'hs') else 'HS' for w in words]
        return " ".join(new_words)
    except:
        return string.capwords(x)

def scroll_shim(element, browser):
    x = element.location['x']
    y = element.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    browser.execute_script(scroll_by_coord)
    browser.execute_script(scroll_nav_out_of_way)
    time.sleep(1)
    return "Scrolled!"

def scroll(element, browser):
    x = element.location['x']
    y = element.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    browser.execute_script(scroll_by_coord)
    time.sleep(1)
    return "Scrolled!"

def scroll_xpath(xpath, browser, num=0, delay=30):
    WebDriverWait(browser, delay).until(
        EC.visibility_of_element_located( (By.XPATH, xpath) ) )
    el = browser.find_elements_by_xpath(xpath)[num]
    scroll_shim(el, browser)
    return "Waited & Scrolled!"

def click_link_by_text(link_text, browser):
    WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable(
        (By.PARTIAL_LINK_TEXT,link_text)))
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located(
        (By.PARTIAL_LINK_TEXT,link_text)))
    browser.find_element_by_partial_link_text(link_text).click()
    return "Clicked!"

def scroll_click_xp(xpath, browser, num=0, delay=30):
    WebDriverWait(browser, delay).until(
        EC.visibility_of_element_located( (By.XPATH, xpath) ) )
    time.sleep(0.5)
    scroll_xpath(xpath, browser, num = num, delay = delay)
    browser.find_elements_by_xpath(xpath)[num].click()
    return "Waited, Scrolled, & Clicked!"

def wait_click_xp(xpath, browser, num=0, delay=30):
    WebDriverWait(browser, delay).until(
        EC.visibility_of_element_located(
        (By.XPATH, xpath)))
    time.sleep(1)
    browser.find_elements_by_xpath(xpath)[num].click()
    return "Waited & Clicked"

def click_xpath(xpath, browser):
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located(
        (By.XPATH, xpath)))
    action = ActionChains(browser)
    action.move_to_element_with_offset(
        browser.find_element_by_xpath(xpath), 0, 0)
    action.click()
    action.perform()
    return "Clicked!"

def click_text(text, browser):
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located(
        (By.XPATH, "//*[contains(text(), '{}')]".format(text))))
    action = ActionChains(browser)
    action.move_to_element_with_offset(
        browser.find_element_by_xpath("//*[contains(text(), '{}')]".format(text)), 5, 5)
    action.click()
    action.perform()
    return "Clicked"

def add_key_to_field(key, element):
    current_text = element.get_attribute("value")
    new_text = current_text + key
    loop = 0
    while element.get_attribute("value") != new_text:
        element.send_keys(key)
        time.sleep(.1)
        loop += 1
        if loop >= 100:
            raise ValueError("Unable to add new key to field {}".format(el))
            break
    return None

def fill_in_xpath(xpath, text, browser, k=0):
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.XPATH,xpath)))
    field = browser.find_elements_by_xpath(xpath)[k]
    field.clear()
    for t in text:
        add_key_to_field(t, field)
    WebDriverWait(browser, 5).until(lambda browser:
        field.get_attribute('value') == text)
    return "Waited & Filled!"

def scroll_fill(xpath, text, browser, k=0):
    scroll_shim(browser.find_elements_by_xpath(xpath)[k], browser)
    return fill_in_xpath(xpath, text, browser, k)

def scroll_fill_visible(xpath, text, browser, k=0):
    vis = [el for el in browser.find_elements_by_xpath(xpath) if el.is_displayed()]
    scroll_shim(vis[k], browser)
    field = vis[k]
    field.clear()
    for t in text:
        add_key_to_field(t, field)
    WebDriverWait(browser, 5).until(lambda browser:
        field.get_attribute('value') == text)
    return "Filled!"


def has_value(xpath, text, browser):
    try:
        element = browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    print(element.get_attribute("value"),text)
    return element.get_attribute("value") == text

def fill_in_id(id, text, browser):
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.ID,id)))
    field = browser.find_element_by_id(id)
    field.clear()
    field.send_keys(text)
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element_value((By.ID,id),text))
    return "filled"

def pick_option_id(id, browser):
    field = browser.find_element_by_id(id)
    field.click()
    return "selected"

def scroll_fill_element(element, text, browser, clearfield=True):
    scroll_shim(element, browser)
    WebDriverWait(browser, 20).until(
        EC.visibility_of(element))
    element.click()
    if clearfield:
        element.clear()
    for t in text:
        add_key_to_field(t, element)
    return "Filled!"

def fill_simple(el, text, browser):
    el.send_keys(text)
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element_value((By.ID,el.get_attribute('id')),
            text))
    return "Filled!"

def fill_simple_validate(el, text, browser):
    el.clear()
    for t in text:
        add_key_to_field(t, el)
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element_value((By.ID,el.get_attribute('id')),
            text))
    return "Filled!"

def click_options(option_text, browser, n=0):
    WebDriverWait(browser, 20).until(
        lambda browser: browser.find_elements_by_xpath(
                "//div[contains(text(), '{}')]".format(option_text))
        )
    st = browser.find_elements_by_xpath("//div[contains(text(), '{}')]".format(option_text))
    scroll_shim(st[n], browser)
    st[n].click()
    return "Clicked!"

def click_at(el, browser):
    action = ActionChains(browser)
    action.move_to_element(el)
    action.click()
    action.click()
    action.perform()
    return "Clicked!"

def find_displayed(xpath, browser):
  return [k for k in browser.find_elements_by_xpath(xpath) if k.is_displayed()]

def wait_displayed(xpath, browser, quant=1, delay=30):
    try:
        WebDriverWait(browser, delay).until(
            lambda browser: len([k for k in browser.find_elements_by_xpath(xpath)
                if k.is_displayed()]) >= quant
        )
    except:
        raise ValueError("{} is not displayed".format(xpath))
    return "Waited"

def click_displayed(xpath, browser, quant=0, delay=30):
    wait_displayed(xpath, browser, quant+1, delay=delay)
    try:
        [k for k in browser.find_elements_by_xpath(xpath)
                if k.is_displayed()][quant].click()
    except:
        raise ValueError("{} is not clickable".format(xpath))
    return "Waited & Clicked!"

def wait_visible(selector_tuple, browser, delay=30):
    try:
        WebDriverWait(browser, delay).until(
            EC.visibility_of_element_located(selector_tuple)
        )
    except:
        raise ValueError("{} is not visible".format(selector_tuple))
    return "Waited"

def wait_clickable(selector_tuple, browser, delay=20):
    try:
        WebDriverWait(browser, delay).until(
            EC.element_to_be_clickable(selector_tuple)
        )
    except:
        raise ValueError("{} is not clickable".format(selector_tuple))
    return "Waited"

def wait_invisible(selector_tuple, browser, delay=20):
    WebDriverWait(browser, delay).until(
        EC.invisibility_of_element_located(selector_tuple)
    )
    return "Waited"

def down_enter(times, browser):
    for k in range(times):
        ActionChains(browser).send_keys(Keys.DOWN).perform()
        time.sleep(1)
    ActionChains(browser).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    return "Pressed down {} times".format(times)

def up_enter(times, browser):
    for k in range(times):
        ActionChains(browser).send_keys(Keys.UP).perform()
        time.sleep(1)
    ActionChains(browser).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    return "Pressed down {} times".format(times)
