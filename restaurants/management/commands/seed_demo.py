from django.core.management.base import BaseCommand
from restaurants.models import Restaurant, MenuItem, Coupon

# 13 categories x 5 independent demo restaurants = 65 restaurants.
RESTAURANT_GROUPS = [
    ("biryani", "Biryani, Hyderabadi", [
        ("Hyderabad Spice House", False), ("Deccan Dum Biryani", False),
        ("Nizam Pot Kitchen", False), ("Royal Handi Biryani", False), ("Charminar Biryani Point", False),
    ]),
    ("shawarma", "Shawarma, Arabian", [
        ("Arabian Nights Grill", False), ("Shawarma Street", False), ("Al Madina Wrap House", False),
        ("Saffron Arabia", False), ("Smoky Pita Co.", False),
    ]),
    ("chinese", "Chinese, Noodles", [
        ("Wok Republic", False), ("Noodle Junction", False), ("Dragon Wok", False),
        ("Street Wok Kitchen", False), ("Schezwan Station", False),
    ]),
    ("southindian", "South Indian, Breakfast", [
        ("Dosa & Co.", True), ("Tiffin Trails", True), ("Udupi Pure Kitchen", True),
        ("Idli Factory", True), ("Ghee Karam Cafe", False),
    ]),
    ("pizza", "Pizza, Italian", [
        ("Pizza Workshop", False), ("Crust & Co.", False), ("Red Oven Pizzeria", False),
        ("Mozzarella Street", False), ("Pizza Borough", False),
    ]),
    ("burger", "Burgers, Fast Food", [
        ("Burger Junction", False), ("Bun & Beyond", False), ("Stack House", False),
        ("Smash Burger Lab", False), ("The Big Bite", False),
    ]),
    ("rolls", "Rolls, Kebabs, Street Food", [
        ("Roll Nation", False), ("Kathi Roll Corner", False), ("Grill & Roll", False),
        ("Kebab Caravan", False), ("Spice Skewers", False),
    ]),
    ("momos", "Momos, Asian", [
        ("Himalayan Momos", False), ("Momos Machine", False), ("Steamy Dumpling House", False),
        ("Tandoori Momo Spot", False), ("Kathmandu Kitchen", False),
    ]),
    ("punjabi", "North Indian, Punjabi", [
        ("Punjabi Tadka", False), ("Butter & Naan", False), ("Dhaba Express", False),
        ("Curry Courtyard", False), ("Punjab Junction", False),
    ]),
    ("cafe", "Cafe, Desserts, Beverages", [
        ("Sweet Cloud Cafe", True), ("Cocoa Cloud", True), ("Waffle Habitat", True),
        ("Sugar Therapy", True), ("Brew Bean Cafe", True),
    ]),
    ("healthy", "Healthy Food, Salads", [
        ("Green Bowl Kitchen", True), ("Millet & More", True), ("Veggie Junction", True),
        ("Fresh Fork", True), ("Satvik Kitchen", True),
    ]),
    ("street", "Street Food, Snacks, Chaat", [
        ("Hyderabad Street Bites", False), ("Frankie Point", False), ("Chaat Bazaar", True),
        ("Fries Station", True), ("Snack Attack", False),
    ]),
    ("coastal", "Andhra, Coastal, Seafood", [
        ("Coastal Fry House", False), ("Andhra Spice Kitchen", False), ("Pepper Chicken Hub", False),
        ("Coastal Curry Bowl", False), ("Fish & Fire", False),
    ]),
]

MENUS = {
    "biryani": [
        ("Chicken Dum Biryani", 260, False, "Aromatic basmati rice with dum-cooked chicken."),
        ("Mutton Biryani", 340, False, "Slow-cooked mutton, spices and fragrant rice."),
        ("Egg Biryani", 190, False, "Spiced rice with boiled eggs."),
        ("Paneer Biryani", 220, True, "Paneer and aromatic masala rice."),
        ("Veg Dum Biryani", 180, True, "Seasonal vegetables cooked dum-style."),
        ("Chicken 65", 210, False, "Crispy, spicy chicken bites."),
        ("Mirchi Ka Salan", 90, True, "Classic peanut and chilli curry."),
        ("Double Ka Meetha", 100, True, "Hyderabadi bread pudding dessert."),
    ],
    "shawarma": [
        ("Classic Chicken Shawarma", 160, False, "Juicy chicken wrapped with garlic sauce."),
        ("Peri Peri Chicken Shawarma", 190, False, "Spicy chicken wrap with house sauce."),
        ("Paneer Shawarma", 150, True, "Grilled paneer, salad and creamy sauce."),
        ("Falafel Pita Roll", 140, True, "Crispy falafel and fresh vegetables."),
        ("Hummus & Pita", 130, True, "Creamy hummus with warm pita bread."),
        ("Masala Fries", 100, True, "Golden fries with a spicy seasoning."),
        ("Chicken Cheese Roll", 175, False, "Chicken, cheese and crunchy vegetables."),
        ("Mint Lemon Cooler", 75, True, "Fresh lime and mint drink."),
    ],
    "chinese": [
        ("Veg Hakka Noodles", 160, True, "Wok-tossed noodles and crisp vegetables."),
        ("Chicken Hakka Noodles", 210, False, "Noodles tossed with chicken and sauces."),
        ("Schezwan Fried Rice", 175, True, "Spicy rice with signature Schezwan sauce."),
        ("Chilli Chicken", 230, False, "Indo-Chinese chicken with peppers."),
        ("Veg Manchurian", 170, True, "Vegetable dumplings in savoury sauce."),
        ("Paneer Chilli", 200, True, "Paneer tossed with chilli and peppers."),
        ("Chicken Momos", 180, False, "Steamed dumplings with chicken filling."),
        ("Hot & Sour Soup", 100, True, "Tangy soup with vegetables."),
    ],
    "southindian": [
        ("Masala Dosa", 110, True, "Crisp dosa with potato masala."),
        ("Idli (4 pcs)", 80, True, "Soft steamed idlis with chutney and sambar."),
        ("Ghee Karam Dosa", 140, True, "Crisp dosa with ghee and spicy podi."),
        ("Pesarattu", 120, True, "Green gram dosa served with ginger chutney."),
        ("Egg Dosa", 130, False, "Dosa with egg and pepper seasoning."),
        ("Medu Vada", 85, True, "Crispy lentil doughnuts with chutney."),
        ("Chicken 65", 210, False, "Spicy fried chicken bites."),
        ("Filter Coffee", 55, True, "South Indian filter coffee."),
    ],
    "pizza": [
        ("Classic Margherita", 220, True, "Tomato, basil and mozzarella."),
        ("Farmhouse Pizza", 310, True, "Peppers, onion, mushroom and cheese."),
        ("Paneer Tikka Pizza", 330, True, "Tandoori paneer and melted cheese."),
        ("BBQ Chicken Pizza", 370, False, "Chicken, smoky sauce and mozzarella."),
        ("Chicken Pepperoni Pizza", 390, False, "Pepperoni, herbs and cheese."),
        ("Garlic Bread", 130, True, "Toasted garlic bread with herbs."),
        ("Pasta Alfredo", 240, True, "Creamy white-sauce pasta."),
        ("Chocolate Brownie", 110, True, "Warm chocolate brownie."),
    ],
    "burger": [
        ("Classic Veg Burger", 130, True, "Vegetable patty, lettuce and house sauce."),
        ("Paneer Crunch Burger", 175, True, "Crispy paneer patty with creamy sauce."),
        ("Crispy Chicken Burger", 190, False, "Crispy chicken fillet and fresh lettuce."),
        ("Chicken Cheese Burger", 220, False, "Chicken patty, cheese and signature sauce."),
        ("Loaded Masala Fries", 125, True, "Fries topped with spices and sauce."),
        ("Chicken Nuggets", 170, False, "Crispy bite-sized chicken."),
        ("Cold Coffee", 110, True, "Chilled coffee blended with milk."),
        ("Chocolate Shake", 140, True, "Thick chocolate milkshake."),
    ],
    "rolls": [
        ("Paneer Kathi Roll", 160, True, "Spiced paneer and crunchy onion wrap."),
        ("Egg Roll", 110, False, "Egg-coated paratha with onion and sauce."),
        ("Chicken Tikka Roll", 190, False, "Tandoori chicken wrapped in a paratha."),
        ("Soya Chaap Roll", 155, True, "Smoky soya chaap with mint chutney."),
        ("Seekh Kebab Roll", 210, False, "Kebab, onion and chutney in a wrap."),
        ("Veg Frankie", 120, True, "Vegetable filling in a soft flatbread."),
        ("Masala Fries", 95, True, "Seasoned potato fries."),
        ("Mint Lassi", 85, True, "Cooling yoghurt drink with mint."),
    ],
    "momos": [
        ("Veg Steamed Momos", 120, True, "Steamed vegetable dumplings."),
        ("Paneer Tandoori Momos", 170, True, "Paneer momos with tandoori seasoning."),
        ("Chicken Steamed Momos", 150, False, "Steamed chicken dumplings."),
        ("Chicken Fried Momos", 180, False, "Crispy fried chicken dumplings."),
        ("Chilli Potato", 145, True, "Crispy potato tossed in chilli sauce."),
        ("Veg Thukpa", 160, True, "Warm noodle soup with vegetables."),
        ("Chicken Thukpa", 195, False, "Noodle soup with chicken."),
        ("Lemon Iced Tea", 75, True, "Refreshing iced tea with lemon."),
    ],
    "punjabi": [
        ("Paneer Butter Masala", 230, True, "Paneer in a creamy tomato gravy."),
        ("Dal Makhani", 210, True, "Slow-cooked black lentils and cream."),
        ("Butter Naan (2 pcs)", 90, True, "Soft naan brushed with butter."),
        ("Chicken Tikka Masala", 290, False, "Tandoori chicken in a rich gravy."),
        ("Butter Chicken", 310, False, "Classic chicken curry in tomato-butter sauce."),
        ("Jeera Rice", 140, True, "Basmati rice tempered with cumin."),
        ("Tandoori Chicken", 280, False, "Roasted chicken with tandoori spices."),
        ("Veg Pulao", 170, True, "Fragrant rice with vegetables."),
    ],
    "cafe": [
        ("Chocolate Brownie", 120, True, "Rich chocolate brownie."),
        ("Classic Cheesecake", 180, True, "Creamy cheesecake slice."),
        ("Belgian Waffle", 190, True, "Warm waffle with chocolate drizzle."),
        ("Cold Coffee", 120, True, "Chilled coffee topped with foam."),
        ("Veg Grilled Sandwich", 150, True, "Toasted sandwich with fresh vegetables."),
        ("Penne Arrabbiata", 220, True, "Penne pasta in spicy tomato sauce."),
        ("Chicken Club Sandwich", 210, False, "Chicken, egg and salad sandwich."),
        ("Blueberry Muffin", 95, True, "Soft baked muffin with blueberry."),
    ],
    "healthy": [
        ("Protein Power Bowl", 220, True, "Grains, beans, greens and house dressing."),
        ("Garden Salad", 160, True, "Fresh seasonal vegetables and seeds."),
        ("Roasted Veg Wrap", 170, True, "Roasted vegetables in a whole-wheat wrap."),
        ("Paneer Grain Bowl", 230, True, "Paneer with grains and seasonal vegetables."),
        ("Chickpea Salad", 175, True, "Chickpeas, herbs and lemon dressing."),
        ("Fruit & Yoghurt Bowl", 145, True, "Fresh fruit and plain yoghurt."),
        ("Millet Upma", 135, True, "Light millet upma with vegetables."),
        ("Fresh Lime Water", 60, True, "Fresh lime with chilled water."),
    ],
    "street": [
        ("Pani Puri (6 pcs)", 60, True, "Crispy puris with tangy flavoured water."),
        ("Dahi Puri", 85, True, "Puris topped with yoghurt and chutneys."),
        ("Pav Bhaji", 130, True, "Spiced vegetable mash with buttered pav."),
        ("Veg Cheese Sandwich", 120, True, "Grilled sandwich with cheese and vegetables."),
        ("Egg Frankie", 110, False, "Egg wrap with onion and sauces."),
        ("Chicken Frankie", 160, False, "Chicken wrap with spices and chutney."),
        ("Samosa (2 pcs)", 50, True, "Crispy potato-filled samosas."),
        ("Masala Lemon Soda", 65, True, "Sparkling lemon drink with spices."),
    ],
    "coastal": [
        ("Fish Fry", 260, False, "Crispy fish with coastal spices."),
        ("Prawns Curry", 320, False, "Prawns in a spicy coastal gravy."),
        ("Gongura Chicken", 290, False, "Andhra chicken curry with gongura."),
        ("Andhra Veg Meals", 180, True, "Rice, seasonal curries and accompaniments."),
        ("Paneer Pepper Fry", 220, True, "Paneer tossed with pepper and spices."),
        ("Chicken Fry Biryani", 280, False, "Spiced chicken fry served with rice."),
        ("Egg Masala", 150, False, "Boiled eggs cooked in masala gravy."),
        ("Steamed Rice", 80, True, "Steamed rice serving."),
    ],
}

IMAGES = {
    "biryani": "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=1000&q=80",
    "shawarma": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?auto=format&fit=crop&w=1000&q=80",
    "chinese": "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=1000&q=80",
    "southindian": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=1000&q=80",
    "pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=1000&q=80",
    "burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1000&q=80",
    "rolls": "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1000&q=80",
    "momos": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=1000&q=80",
    "punjabi": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=1000&q=80",
    "cafe": "https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=1000&q=80",
    "healthy": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1000&q=80",
    "street": "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=1000&q=80",
    "coastal": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=1000&q=80",
}

DESCRIPTIONS = {
    "biryani": "Aromatic dum biryani, classic sides and rich regional flavours.",
    "shawarma": "Fresh wraps, grilled fillings and bold Middle Eastern sauces.",
    "chinese": "Wok-tossed noodles, rice bowls and Indo-Chinese favourites.",
    "southindian": "Crisp dosas, fluffy idlis, chutneys and comforting tiffins.",
    "pizza": "Oven-baked pizzas, cheesy sides and Italian-inspired comfort food.",
    "burger": "Burgers, crispy sides and satisfying fast-food favourites.",
    "rolls": "Street-style wraps, rolls, kebabs and spicy sides.",
    "momos": "Steamed dumplings, spicy sauces and warm Asian comfort food.",
    "punjabi": "North Indian curries, tandoori dishes, naan and fragrant rice.",
    "cafe": "Coffee, bakes, desserts and easy cafe-style meals.",
    "healthy": "Fresh bowls, salads, whole grains and feel-good vegetarian meals.",
    "street": "Popular Indian street snacks, chaat, rolls and refreshing drinks.",
    "coastal": "Andhra spices, coastal curries, seafood and regional favourites.",
}

class Command(BaseCommand):
    help = "Create 65 demo restaurants with varied vegetarian and non-vegetarian menus plus test coupons."

    def handle(self, *args, **options):
        restaurant_count = 0
        for theme_index, (theme, cuisines, names) in enumerate(RESTAURANT_GROUPS):
            for index, (name, pure_veg) in enumerate(names):
                restaurant, _ = Restaurant.objects.update_or_create(name=name, defaults={
                    "cuisines": cuisines, "description": DESCRIPTIONS[theme],
                    "address": ["Kukatpally, Hyderabad", "Balanagar, Hyderabad", "Miyapur, Hyderabad", "Hitech City, Hyderabad", "Ameerpet, Hyderabad"][index % 5],
                    "image_url": IMAGES[theme], "rating": f"{4.0 + ((theme_index + index) % 9) / 10:.1f}",
                    "delivery_minutes": 20 + ((theme_index * 3 + index * 4) % 26),
                    "cost_for_two": 250 + ((theme_index * 37 + index * 55) % 550),
                    "is_vegetarian": pure_veg, "is_featured": index == 0 or (theme_index + index) % 7 == 0,
                    "is_active": True,
                })
                expected_menu_names = []
                for dish_name, price, vegetarian, description in MENUS[theme]:
                    if pure_veg and not vegetarian:
                        continue
                    expected_menu_names.append(dish_name)
                    MenuItem.objects.update_or_create(restaurant=restaurant, name=dish_name, defaults={
                        "price": price, "is_vegetarian": vegetarian, "description": description, "is_available": True,
                    })
                # Keep reseeding deterministic when an older version of this demo database exists.
                MenuItem.objects.filter(restaurant=restaurant).exclude(name__in=expected_menu_names).delete()
                restaurant_count += 1
        Coupon.objects.update_or_create(code="FOODIE10", defaults={
            "description": "10% off food subtotal (up to ₹100)", "discount_type": "percent",
            "discount_value": 10, "minimum_subtotal": 0, "max_discount": 100, "is_active": True,
        })
        Coupon.objects.update_or_create(code="WELCOME50", defaults={
            "description": "₹50 off orders of ₹250 or more", "discount_type": "fixed",
            "discount_value": 50, "minimum_subtotal": 250, "max_discount": 50, "is_active": True,
        })
        self.stdout.write(self.style.SUCCESS(f"Seeded {restaurant_count} demo restaurants, menu items, and coupons."))
