from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Cheese, Base, CheeseItem, User

engine = create_engine('sqlite:///cheesewithuser.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
# creating user
user1 = User(name="admin", email="mounisha.nsp@gmail.com")
session.add(user1)
session.commit()
# cheese country1
cheese1 = Cheese(name="Asian cheese", user_id=1)

session.add(cheese1)
session.commit()
# cheese Item1
cheeseItem1 = CheeseItem(name="Chhana cheese", description="A fresh, unripened"
                         "curd cheese made from cow or water buffalo milk",
                         price="$25", cheese=cheese1, user_id=1)

session.add(cheeseItem1)
session.commit()

# cheese item2
cheeseItem2 = CheeseItem(name="Kalari cheese", description="Also known as"
                         "Kiladi or Maish Krej from Kashmiri",
                         price="$30", cheese=cheese1, user_id=1)

session.add(cheeseItem2)
session.commit()
# cheese item3
cheeseItem3 = CheeseItem(name="Bandel cheese", description="originated in a"
                         "Portuguese colony Bandel located in eastern India",
                         price="$10", cheese=cheese1, user_id=1)

session.add(cheeseItem3)
session.commit()
# cheese item4
cheeseItem4 = CheeseItem(name="Sakura cheese", description="A soft cheese"
                         "created in Japan. It is creamy white and"
                         "flavored with mountain cherry leaves.",
                         price="$39", cheese=cheese1, user_id=1)

session.add(cheeseItem4)
session.commit()
# cheese item5
cheeseItem5 = CheeseItem(name="Imsil cheese", description="Imsil Cheese"
                         "Village is located near the town of Imsil."
                         "It offers programs lasting for one day or more,"
                         "in which guests learn how to make cheese.",
                         price="$28", cheese=cheese1, user_id=1)

session.add(cheeseItem5)
session.commit()

# cheese country2
cheese2 = Cheese(name="South American cheese", user_id=1)

session.add(cheese2)
session.commit()
# cheese item1
cheeseItem1 = CheeseItem(name="Cremoso cheese", description="A fresh"
                         "cheese elaborated with cow's milk, with or"
                         "without the addition of cream.",
                         price="$30", cheese=cheese2, user_id=1)

session.add(cheeseItem1)
session.commit()

# cheese item2
cheeseItem2 = CheeseItem(name="Catupiry cheese", description="A soft,"
                         " mild-tasting cheese that can be spread over toasts,"
                         "crackers and bread buns or used in cooking.",
                         price="$35", cheese=cheese2, user_id=1)

session.add(cheeseItem2)
session.commit()
# cheese item3
cheeseItem3 = CheeseItem(name="Chanco cheese", description="Cow's milk"
                         "cheese originally from the Chanco farm in"
                         "Maule Region.",
                         price="$20", cheese=cheese2, user_id=1)

session.add(cheeseItem3)
session.commit()
# cheese item 4
cheeseItem4 = CheeseItem(name="Panquehue cheese", description="A semi-soft"
                         "cheese, and often has chives or red pepper flakes"
                         "mixed in.",
                         price="$15", cheese=cheese2, user_id=1)

session.add(cheeseItem4)
session.commit()
# cheese item 5
cheeseItem5 = CheeseItem(name="Quesillo cheese", description="In Colombia,"
                         "quesillo is a type of double cream cheese"
                         "wrapped within a plantain leaf.",
                         price="$9.56", cheese=cheese2, user_id=1)

session.add(cheeseItem5)
session.commit()

# cheese country 3
cheese3 = Cheese(name="African cheese", user_id=1)

session.add(cheese3)
session.commit()
# cheese item1
cheeseItem1 = CheeseItem(name="Wagasi cheese", description="It is a soft"
                         "cow milk cheese.",
                         price="$20", cheese=cheese3, user_id=1)

session.add(cheeseItem1)
session.commit()
# cheese item2
cheeseItem2 = CheeseItem(name="Areesh cheese", description="A type of"
                         "white, soft, lactic cheese made from"
                         "laban rayeb.",
                         price="$15", cheese=cheese3, user_id=1)

session.add(cheeseItem2)
session.commit()
# cheese item3
cheeseItem3 = CheeseItem(name="Domiati cheese", description="A soft"
                         "white cheese usually made from cow or"
                         "buffalo milk. It is salted, heated,"
                         "coagulated using rennet and then ladled"
                         "into wooden molds where the whey is"
                         "drained away for three days.",
                         price="$30", cheese=cheese3, user_id=1)

session.add(cheeseItem3)
session.commit()
# cheese item4
cheeseItem4 = CheeseItem(name="Halumi cheese", description="A semi-hard,"
                         "unripened, brined cheese made from a mixture"
                         "of goat's and sheep's milk, and sometimes"
                         "also cow's milk.",
                         price="$10", cheese=cheese3, user_id=1)

session.add(cheeseItem4)
session.commit()
# cheese item 5
cheeseItem5 = CheeseItem(name="Rumi", description="A hard,"
                         "bacterially ripened variety of cheese."
                         "It is salty, with a crumbly texture,"
                         "and is sold at different stages of aging.",
                         price="$25", cheese=cheese3, user_id=1)

session.add(cheeseItem5)
session.commit()

# cheese country 4
cheese4 = Cheese(name="North American cheese", user_id=1)

session.add(cheese4)
session.commit()
# cheese item 1
cheeseItem1 = CheeseItem(name="Cheese curds", description="Cheese curds"
                         "are a key ingredient in poutine.",
                         price="$10", cheese=cheese4, user_id=1)

session.add(cheeseItem1)
session.commit()
# cheese item 2
cheeseItem2 = CheeseItem(name="Oka cheese", description="Originally"
                         "manufactured by the Trappist monks, this"
                         "cheese has a distinct flavour and aroma.",
                         price="$15", cheese=cheese4, user_id=1)

session.add(cheeseItem2)
session.commit()
# cheese item 3
cheeseItem3 = CheeseItem(name="Crema cheese", description="A spreadable,"
                         "unripened white cheese.",
                         price="$20", cheese=cheese4, user_id=1)

session.add(cheeseItem3)
session.commit()
# cheese item 4
cheeseItem4 = CheeseItem(name="Anejo cheese", description="A Mexican cheese"
                         "traditionally made from skimmed goat's milk but"
                         "most often available made from skimmed cow's milk.",
                         price="$25", cheese=cheese4, user_id=1)

session.add(cheeseItem4)
session.commit()
# cheese item 5
cheeseItem5 = CheeseItem(name="Chiapas cheese", description="A dry cream"
                         "cheese with a crumbly texture that is formed"
                         "into balls an often has string cheese"
                         "wrapped around it.",
                         price="$30", cheese=cheese4, user_id=1)

session.add(cheeseItem5)
session.commit()

# cheese country 5
cheese5 = Cheese(name="Sweden cheese", user_id=1)

session.add(cheese5)
session.commit()
# cheese item 1
cheeseItem1 = CheeseItem(name="Greve cheese", description="A semi-hard"
                         "Swedish cheese made from cow's milk."
                         "It is similar to Emmental with a mild"
                         "and nutty taste.",
                         price="$9.67", cheese=cheese5, user_id=1)

session.add(cheeseItem1)
session.commit()
# cheese item2
cheeseItem2 = CheeseItem(name="Herrgardsost cheese", description="A"
                         "semi-hard cheese made from cow's milk."
                         "The aged cheese has a mild, sweet, nutty"
                         "flavor and small round holes.",
                         price="$16.9", cheese=cheese5, user_id=1)

session.add(cheeseItem2)
session.commit()
# cheese item 3
cheeseItem3 = CheeseItem(name="Hushallsost cheese", description="A"
                         "semi-hard cows'-milk cheese with small"
                         "granular holes and aged around 60 days on"
                         "average.",
                         price="$15.5", cheese=cheese5, user_id=1)

session.add(cheeseItem3)
session.commit()
# cheese item 4
cheeseItem4 = CheeseItem(name="Moose cheese", description="A cheese"
                         "produced in Sweden from moose milk",
                         price="$10.5", cheese=cheese5, user_id=1)

session.add(cheeseItem4)
session.commit()
# cheese item 5
cheeseItem5 = CheeseItem(name="Prastost cheese", description="Made from"
                         "pasteurized cow's milk.",
                         price="$5.5", cheese=cheese5, user_id=1)

session.add(cheeseItem5)
session.commit()

print "added cheese items!"
