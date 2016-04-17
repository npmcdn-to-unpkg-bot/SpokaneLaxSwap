# run this file to automatically populate the db with post info

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Posting

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

post_1 = Posting(title = "Brine Clutch",
	description = "weird colors, idk",
	price = 60,
	category = "Stick",
	picture = "post1.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_1)

post_2 = Posting(title = "stringing services",
	description = "I do quality stringjobs. hit me up if you want to sling absolute lasers",
	price = 25,
	category = "Stringing",
	picture = "post2.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_2)

post_3 = Posting(title = "Burnaby Pro 7",
	description = "Great helmet, Has burnaby mountain selects decals on it. Asking 100",
	price = 100,
	category = "Protection",
	picture = "post3.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_3)

post_4 = Posting(title = "Wood Stick",
	description = "Handcrafted by the Mitchell Brothers on mohawk reservation. pretty solid, in good shape",
	price = 150,
	category = "Stick",
	picture = "post4.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_4)

post_5 = Posting(title = "Evo Gloves",
	description = "best gloves on the market, feels like bare skin",
	price = 160,
	category = "Protection",
	picture = "post5.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_5)

post_6 = Posting(title = "Stx assault shoulder pads",
	description = "great protection. Makes you feel like batman",
	price = 80,
	category = "Protection",
	picture = "post6.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_6)

post_7 = Posting(title = "Lone sock",
	description = "pretty old, doesnt have a match",
	price = 1000,
	category = "Apparel",
	picture = "post7.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_7)

post_8 = Posting(title = "White nike shorts",
	description = "pretty swagtastic if you ask me. barely used",
	price = 15,
	category = "Apparel",
	picture = "post8.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_8)

post_9 = Posting(title = "Stringing",
	description = "Looks pretty great if you ask me. will also accept six pack of IPA's as payment",
	price = 20,
	category = "Stringing",
	picture = "post9.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_9)

post_10 = Posting(title = "Mens league",
	description = "Inland Empire lacrosse taking 18+ aged players of all skill levels. Come out and have fun",
	price = 0,
	category = "Misc",
	picture = "post10.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_10)

post_11 = Posting(title = "Dragonfly shaft",
	description = "Great shape, barely used. Flex iq 9",
	price = 120,
	category = "Stick",
	picture = "post11.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_11)

post_12 = Posting(title = "Stx Stallion Arm Guards",
	description = "Awesome, tons of protection, great for middies.",
	price = 60,
	category = "Protection",
	picture = "post12.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_12)

post_13 = Posting(title = "Stx deuce",
	description = "strung like deuce.",
	price = 40,
	category = "Stick",
	picture = "post13.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_13)

post_14 = Posting(title = "Stx Super Power",
	description = "Heavily used but still going strong. Durable and strung well",
	price = 50,
	category = "Stick",
	picture = "post14.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_14)

post_15 = Posting(title = "Nike Cleats",
	description = "Could be cleaned but still pretty good",
	price = 40,
	category = "Apparel",
	picture = "post15.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_15)

post_16 = Posting(title = "Shooting Sesh",
	description = "Shooting tonight at GU. Anyone is invited, bring some balls",
	price = 0,
	category = "Misc",
	picture = 'default.jpg',
	user_id = 'bushleaguelax@gmail.com')
session.add(post_16)

post_17 = Posting(title = "Inland Empire Pinnie",
	description = "Number 41, nike. Looks pretty fly, size LG",
	price = 25,
	category = "Apparel",
	picture = "post17.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_17)

post_18 = Posting(title = "Stx evo 4x",
	description = "Strung awesome, barely used",
	price = 75,
	category = "Stick",
	picture = "post18.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_18)

post_19 = Posting(title = "Gonzaga Prep Cpxr",
	description = "pretty awesome helmet. has some filthy tilt",
	price = 120,
	category = "Protection",
	picture = "post19.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_19)

post_20 = Posting(title = "BMS lax bro tank",
	description = "pretty fly. red",
	price = 20,
	category = "Apparel",
	picture = "post20.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_20)

post_21 = Posting(title = "Haydens stick",
	description = "Legendary. Graced with the blood sweat and tears of Hayden Thomas. basically a cheat code",
	price = 9999,
	category = "Stick",
	picture = "post21.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_21)

post_22 = Posting(title = "Big cat lax nike jacket",
	description = "New nike weathertek. ",
	price = 100,
	category = "Apparel",
	picture = "post22.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_22)

post_23 = Posting(title = "Blue and white brine clutch",
	description = "Strung with StringKing 2s. Awesome feel",
	price = 80,
	category = "Stick",
	picture = "post23.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_23)

post_24 = Posting(title = "Stx noz 2",
	description = "Limited Edition. never used",
	price = 80,
	category = "Stick",
	picture = "post24.jpg",
	user_id = 'bushleaguelax@gmail.com')
session.add(post_24)


session.commit()