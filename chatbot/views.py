# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import os
# from datetime import datetime, timedelta
# from openai import OpenAI
# import time

# # Selenium imports
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # -------------------- LLM Client --------------------
# client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://openrouter.ai/api/v1")

# # -------------------- Session storage --------------------
# sessions = {}
# messages = {}
# SESSION_TTL_HOURS = 24

# # -------------------- Views --------------------
# def home(request):
#     return render(request, "chatbot/index.html")


# @api_view(["POST"])
# def chat(request):
#     data = request.data
#     session_id = data.get("session_id")
#     user_message = data.get("message", "").strip()
#     current_time = datetime.now()

#     # Session handling
#     is_new_session = False
#     if not session_id or session_id not in sessions:
#         session_id = str(current_time.timestamp())
#         is_new_session = True
#         sessions[session_id] = {"created_at": current_time, "last_activity": current_time}
#         messages[session_id] = []
#     else:
#         sessions[session_id]["last_activity"] = current_time

#     messages[session_id].append({"role": "user", "content": user_message, "timestamp": current_time.isoformat()})

#     # Check for plain t-shirts keyword
#     if "plain t-shirts" in user_message.lower():
#         bot_response = fetch_plain_tshirts()
#     else:
#         bot_response = get_llm_response(messages[session_id])

#     messages[session_id].append({"role": "assistant", "content": bot_response, "timestamp": datetime.now().isoformat()})

#     cleanup_old_sessions()

#     return Response({
#         "session_id": session_id,
#         "is_new_session": is_new_session,
#         "response": bot_response,
#         "messages": messages[session_id]
#     })


# # -------------------- Functions --------------------
# def fetch_plain_tshirts():
#     """
#     Fetch Wix plain t-shirts using Selenium from gallery container
#     """
#     try:
#         options = Options()
#         options.headless = True
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")

#         service = Service()
#         driver = webdriver.Chrome(service=service, options=options)

#         url = "https://palpurna55.wixsite.com/karnamaa1/plain-t-shirts-for-men"
#         driver.get(url)

#         # Wait for gallery container to load
#         WebDriverWait(driver, 15).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-hook='gallery-app-container']"))
#         )

#         # Scroll to bottom to load all lazy-loaded items
#         last_height = driver.execute_script("return document.body.scrollHeight")
#         while True:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2)
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height

#         products = []
#         gallery = driver.find_element(By.CSS_SELECTOR, "div[data-hook='gallery-app-container']")
#         items = gallery.find_elements(By.CSS_SELECTOR, "div")  # adjust if Wix uses specific classes for items

#         for item in items:
#             try:
#                 name = item.find_element(By.CSS_SELECTOR, "h3").text
#             except:
#                 name = "N/A"
#             try:
#                 price = item.find_element(By.CSS_SELECTOR, "span").text
#             except:
#                 price = "N/A"
#             try:
#                 img = item.find_element(By.TAG_NAME, "img").get_attribute("src")
#             except:
#                 img = "N/A"

#             if name != "N/A" or img != "N/A":
#                 products.append({"name": name, "price": price, "image": img})

#         driver.quit()

#         if not products:
#             return "⚠️ No products found."
#         return products

#     except Exception as e:
#         return f"⚠️ Failed to fetch products: {str(e)}"


# def get_llm_response(conversation_history):
#     messages_payload = [{"role": msg['role'], "content": msg['content']} for msg in conversation_history]
#     try:
#         response = client.chat.completions.create(
#             model="deepseek/deepseek-chat",
#             messages=messages_payload,
#             temperature=0.7,
#             max_tokens=300
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         if "402" in str(e) or "Insufficient Balance" in str(e):
#             try:
#                 response = client.chat.completions.create(
#                     model="openai/gpt-3.5-turbo",
#                     messages=messages_payload,
#                     temperature=0.7,
#                     max_tokens=300
#                 )
#                 return response.choices[0].message.content.strip()
#             except Exception as inner_e:
#                 return f"⚠️ Both DeepSeek and GPT-3.5 failed: {str(inner_e)}"
#         return f"⚠️ LLM API call failed: {str(e)}"


# def cleanup_old_sessions():
#     current_time = datetime.now()
#     expired = [sid for sid, data in sessions.items() if current_time - data["last_activity"] > timedelta(hours=SESSION_TTL_HOURS)]
#     for sid in expired:
#         sessions.pop(sid, None)
#         messages.pop(sid, None)


# # -------------------- Wix Products API --------------------
# @api_view(["GET"])
# def wix_products_api(request):
#     """
#     API endpoint to fetch Wix plain t-shirts products in JSON
#     """
#     products = fetch_plain_tshirts()
#     if isinstance(products, str):
#         return Response({"error": products}, status=400)
#     return Response({"products": products})

# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import os
# from datetime import datetime, timedelta
# from openai import OpenAI
# from playwright.sync_api import sync_playwright

# # -------------------- LLM Client --------------------
# client = OpenAI(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://openrouter.ai/api/v1"
# )

# # -------------------- Session storage --------------------
# sessions = {}
# messages = {}
# SESSION_TTL_HOURS = 24

# # -------------------- Views --------------------
# def home(request):
#     return render(request, "chatbot/index.html")


# @api_view(["POST"])
# def chat(request):
#     data = request.data
#     session_id = data.get("session_id")
#     user_message = data.get("message", "").strip()
#     current_time = datetime.now()

#     # Session handling
#     is_new_session = False
#     if not session_id or session_id not in sessions:
#         session_id = str(current_time.timestamp())
#         is_new_session = True
#         sessions[session_id] = {"created_at": current_time, "last_activity": current_time}
#         messages[session_id] = []
#     else:
#         sessions[session_id]["last_activity"] = current_time

#     messages[session_id].append({
#         "role": "user",
#         "content": user_message,
#         "timestamp": current_time.isoformat()
#     })

#     # -------------------- Chatbot Logic --------------------
#     if "plain t-shirts" in user_message.lower():
#         bot_response = scrape_wix_plain_tshirts()
#     elif any(word in user_message.lower() for word in ["offer", "offers", "deal", "discount", "sale"]):
#         bot_response = scrape_wix_offers()
#     elif any(word in user_message.lower() for word in ["contact", "address", "office", "email", "phone", "call", "reach out"]):
#         bot_response = get_chatbot_response(user_message)
#     else:
#         bot_response = get_llm_response(messages[session_id])
#     # --------------------------------------------------------

#     messages[session_id].append({
#         "role": "assistant",
#         "content": bot_response,
#         "timestamp": datetime.now().isoformat()
#     })

#     cleanup_old_sessions()

#     return Response({
#         "session_id": session_id,
#         "is_new_session": is_new_session,
#         "response": bot_response,
#         "messages": messages[session_id]
#     })


# # -------------------- Contact Response --------------------
# def get_chatbot_response(user_input: str) -> str:
#     """
#     Returns chatbot response based on user query.
#     """
#     query = user_input.lower()

#     contact_keywords = ["contact", "address", "office", "email", "phone", "call", "reach out"]

#     if any(word in query for word in contact_keywords):
#         return (
#             "📞 **Reach Out – We will get back to you**\n\n"
#             "**KARNAMAA Bengaluru Office**\n\n"
#             "📍 NO: 677, 1st Floor, Suit # 221, 27th Main, 13th Cross, Sector 1, "
#             "HSR Layout, Bangalore-560102\n\n"
#             "📱 Mob: +91 6363857937\n"
#             "📧 Email: info@Karnamaa.com\n\n"
#             "👉 [Click here to Contact Us](https://palpurna55.wixsite.com/karnamaa1/contact)"
#         )

#     return "I’m here to help! Please tell me what you’d like to know."


# # -------------------- LLM Fallback --------------------
# def get_llm_response(conversation_history):
#     messages_payload = [
#         {"role": msg['role'], "content": msg['content']}
#         for msg in conversation_history
#     ]
#     try:
#         response = client.chat.completions.create(
#             model="deepseek/deepseek-chat",
#             messages=messages_payload,
#             temperature=0.7,
#             max_tokens=300
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         if "402" in str(e) or "Insufficient Balance" in str(e):
#             try:
#                 response = client.chat.completions.create(
#                     model="openai/gpt-3.5-turbo",
#                     messages=messages_payload,
#                     temperature=0.7,
#                     max_tokens=300
#                 )
#                 return response.choices[0].message.content.strip()
#             except Exception as inner_e:
#                 return f"⚠️ Both DeepSeek and GPT-3.5 failed: {str(inner_e)}"
#         return f"⚠️ LLM API call failed: {str(e)}"


# def cleanup_old_sessions():
#     current_time = datetime.now()
#     expired = [
#         sid for sid, data in sessions.items()
#         if current_time - data["last_activity"] > timedelta(hours=SESSION_TTL_HOURS)
#     ]
#     for sid in expired:
#         sessions.pop(sid, None)
#         messages.pop(sid, None)


# # -------------------- Wix Scraper: Plain T-Shirts --------------------
# def scrape_wix_plain_tshirts():
#     url = "https://palpurna55.wixsite.com/karnamaa1/plain-t-shirts-for-men"
#     products = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url, timeout=60000)
#         page.wait_for_selector('[data-hook="product-item-name-and-price-layout"]', timeout=30000)
#         product_elements = page.query_selector_all('[data-hook="product-item-name-and-price-layout"]')

#         for el in product_elements:
#             try:
#                 name_el = el.query_selector('[data-hook="product-item-name"]')
#                 name = name_el.inner_text().strip() if name_el else "N/A"

#                 price_before = el.query_selector('[data-hook="product-item-price-before-discount"]')
#                 regular_price = price_before.inner_text().strip() if price_before else "N/A"

#                 price_sale = el.query_selector('[data-hook="product-item-price-to-pay"]')
#                 sale_price = price_sale.inner_text().strip() if price_sale else "N/A"

#                 img_el = el.query_selector('img')
#                 img_url = img_el.get_attribute('src') if img_el else ""

#                 link_el = el.query_selector('a')
#                 product_url = link_el.get_attribute('href') if link_el else url

#                 products.append({
#                     "name": name,
#                     "regular_price": regular_price,
#                     "sale_price": sale_price,
#                     "image": img_url,
#                     "url": product_url
#                 })
#             except:
#                 continue
#         browser.close()
#     return products


# # -------------------- Wix Scraper: Offers --------------------
# def scrape_wix_offers():
#     url = "https://palpurna55.wixsite.com/karnamaa1/offers"
#     offers = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url, timeout=60000)

#         # NOTE: You must inspect actual HTML of "offers" page to confirm selectors
#         page.wait_for_selector('[data-hook="product-item-name-and-price-layout"]', timeout=30000)
#         offer_elements = page.query_selector_all('[data-hook="product-item-name-and-price-layout"]')

#         for el in offer_elements:
#             try:
#                 title_el = el.query_selector('[data-hook="product-item-name"]')
#                 title = title_el.inner_text().strip() if title_el else "N/A"

#                 price_el = el.query_selector('[data-hook="product-item-price-to-pay"]')
#                 price = price_el.inner_text().strip() if price_el else "N/A"

#                 img_el = el.query_selector('img')
#                 img = img_el.get_attribute('src') if img_el else ""

#                 link_el = el.query_selector('a')
#                 link = link_el.get_attribute('href') if link_el else url

#                 offers.append({
#                     "title": title,
#                     "price": price,
#                     "image": img,
#                     "url": link
#                 })
#             except:
#                 continue
#         browser.close()
#     return offers

# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import os
# from datetime import datetime, timedelta
# from openai import OpenAI
# from playwright.sync_api import sync_playwright

# # -------------------- LLM Client --------------------
# client = OpenAI(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://openrouter.ai/api/v1"
# )

# # -------------------- Session storage --------------------
# sessions = {}
# messages = {}
# SESSION_TTL_HOURS = 24

# # -------------------- Views --------------------
# def home(request):
#     return render(request, "chatbot/index.html")


# @api_view(["POST"])
# def chat(request):
#     data = request.data
#     session_id = data.get("session_id")
#     user_message = data.get("message", "").strip()
#     current_time = datetime.now()

#     # Session handling
#     is_new_session = False
#     if not session_id or session_id not in sessions:
#         session_id = str(current_time.timestamp())
#         is_new_session = True
#         sessions[session_id] = {
#             "created_at": current_time,
#             "last_activity": current_time
#         }
#         messages[session_id] = []
#     else:
#         sessions[session_id]["last_activity"] = current_time

#     # Store user message
#     messages[session_id].append({
#         "role": "user",
#         "content": user_message,
#         "timestamp": current_time.isoformat()
#     })

#     # -------------------- Chatbot Logic --------------------
#     user_lower = user_message.lower()
#     if "plain t-shirts" in user_lower:
#         bot_response = scrape_wix_plain_tshirts()
#     elif "women t-shirts" in user_lower:
#         bot_response = scrape_wix_women_tshirts()
#     elif "sweatshirts" in user_lower or "hoodies" in user_lower:
#         bot_response = scrape_wix_sweatshirts()
#     elif any(word in user_lower for word in ["offer", "offers", "deal", "discount", "sale"]):
#         bot_response = scrape_wix_offers()
#     elif any(word in user_lower for word in ["design lab", "lab design", "custom design"]):
#         bot_response = scrape_wix_design_lab()
#     elif any(word in user_lower for word in ["contact", "address", "office", "email", "phone", "call", "reach out"]):
#         bot_response = get_chatbot_response(user_message)
#     else:
#         bot_response = get_llm_response(messages[session_id])
#     # --------------------------------------------------------

#     # Store assistant response
#     messages[session_id].append({
#         "role": "assistant",
#         "content": bot_response,
#         "timestamp": datetime.now().isoformat()
#     })

#     cleanup_old_sessions()

#     return Response({
#         "session_id": session_id,
#         "is_new_session": is_new_session,
#         "response": bot_response,
#         "messages": messages[session_id]
#     })


# # -------------------- Contact Response --------------------
# def get_chatbot_response(user_input: str) -> str:
#     query = user_input.lower()
#     contact_keywords = ["contact", "address", "office", "email", "phone", "call", "reach out"]

#     if any(word in query for word in contact_keywords):
#         return (
#             "📞 **Reach Out – We will get back to you**\n\n"
#             "**KARNAMAA Bengaluru Office**\n\n"
#             "📍 NO: 677, 1st Floor, Suit # 221, 27th Main, 13th Cross, Sector 1, "
#             "HSR Layout, Bangalore-560102\n\n"
#             "📱 Mob: +91 6363857937\n"
#             "📧 Email: info@Karnamaa.com\n\n"
#             "👉 [Click here to Contact Us](https://palpurna55.wixsite.com/karnamaa1/contact)"
#         )

#     return "I’m here to help! Please tell me what you’d like to know."


# # -------------------- LLM Fallback --------------------
# def get_llm_response(conversation_history):
#     messages_payload = [
#         {"role": msg['role'], "content": msg['content']}
#         for msg in conversation_history
#     ]
#     try:
#         response = client.chat.completions.create(
#             model="deepseek/deepseek-chat",
#             messages=messages_payload,
#             temperature=0.7,
#             max_tokens=300
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         if "402" in str(e) or "Insufficient Balance" in str(e):
#             try:
#                 response = client.chat.completions.create(
#                     model="openai/gpt-3.5-turbo",
#                     messages=messages_payload,
#                     temperature=0.7,
#                     max_tokens=300
#                 )
#                 return response.choices[0].message.content.strip()
#             except Exception as inner_e:
#                 return f"⚠️ Both DeepSeek and GPT-3.5 failed: {str(inner_e)}"
#         return f"⚠️ LLM API call failed: {str(e)}"


# # -------------------- Cleanup Old Sessions --------------------
# def cleanup_old_sessions():
#     current_time = datetime.now()
#     expired = [
#         sid for sid, data in sessions.items()
#         if current_time - data["last_activity"] > timedelta(hours=SESSION_TTL_HOURS)
#     ]
#     for sid in expired:
#         sessions.pop(sid, None)
#         messages.pop(sid, None)


# # -------------------- Wix Scraper: Plain T-Shirts --------------------
# def scrape_wix_plain_tshirts():
#     url = "https://palpurna55.wixsite.com/karnamaa1/plain-t-shirts-for-men"
#     return scrape_wix_generic(url)


# # -------------------- Wix Scraper: Women T-Shirts --------------------
# def scrape_wix_women_tshirts():
#     url = "https://palpurna55.wixsite.com/karnamaa1/women-t-shirts"
#     return scrape_wix_generic(url)


# # -------------------- Wix Scraper: Sweatshirts & Hoodies --------------------
# def scrape_wix_sweatshirts():
#     url = "https://palpurna55.wixsite.com/karnamaa1/sweatshirts-hoodies"
#     return scrape_wix_generic(url)


# # -------------------- Wix Scraper: Offers --------------------
# def scrape_wix_offers():
#     url = "https://palpurna55.wixsite.com/karnamaa1/offers"
#     return scrape_wix_generic(url)


# # -------------------- Wix Scraper: Design Lab --------------------
# def scrape_wix_design_lab():
#     url = "https://palpurna55.wixsite.com/karnamaa1/design-lab"
#     return scrape_wix_generic(url)

# # # def ():
# # #     url="https://palpurna55.wixsite.com/karnamaa1/blog"
# #     return scrape_wix_generic(url)
# # -------------------- Generic Wix Scraper --------------------


# def scrape_wix_generic(url):
#     items = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url, timeout=60000)
#         page.wait_for_selector('[data-hook="product-item-name-and-price-layout"]', timeout=30000)
#         product_elements = page.query_selector_all('[data-hook="product-item-name-and-price-layout"]')

#         for el in product_elements:
#             try:
#                 name_el = el.query_selector('[data-hook="product-item-name"]')
#                 name = name_el.inner_text().strip() if name_el else "N/A"

#                 price_before = el.query_selector('[data-hook="product-item-price-before-discount"]')
#                 regular_price = price_before.inner_text().strip() if price_before else "N/A"

#                 price_sale = el.query_selector('[data-hook="product-item-price-to-pay"]')
#                 sale_price = price_sale.inner_text().strip() if price_sale else "N/A"

#                 img_el = el.query_selector("img")
#                 img_url = img_el.get_attribute("src") if img_el else ""

#                 link_el = el.query_selector("a")
#                 product_url = link_el.get_attribute("href") if link_el else url

#                 items.append({
#                     "name": name,
#                     "regular_price": regular_price,
#                     "sale_price": sale_price,
#                     "image": img_url,
#                     "url": product_url
#                 })
#             except Exception as e:
#                 print("Error scraping item:", e)
#                 continue

#         browser.close()
#     return items

# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import os
# from datetime import datetime, timedelta
# from openai import OpenAI
# from playwright.sync_api import sync_playwright

# # -------------------- LLM Client --------------------
# client = OpenAI(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://openrouter.ai/api/v1"
# )

# # -------------------- Session storage --------------------
# sessions = {}
# messages = {}
# SESSION_TTL_HOURS = 24

# # -------------------- Views --------------------
# def home(request):
#     return render(request, "chatbot/index.html")


# @api_view(["POST"])
# def chat(request):
#     data = request.data
#     session_id = data.get("session_id")
#     user_message = data.get("message", "").strip()
#     current_time = datetime.now()

#     # Session handling
#     is_new_session = False
#     if not session_id or session_id not in sessions:
#         session_id = str(current_time.timestamp())
#         is_new_session = True
#         sessions[session_id] = {
#             "created_at": current_time,
#             "last_activity": current_time
#         }
#         messages[session_id] = []
#     else:
#         sessions[session_id]["last_activity"] = current_time

#     # Store user message
#     messages[session_id].append({
#         "role": "user",
#         "content": user_message,
#         "timestamp": current_time.isoformat()
#     })

#     # -------------------- Chatbot Logic --------------------
#     user_lower = user_message.lower()
#     if "plain t-shirts" in user_lower:
#         bot_response = scrape_wix_plain_tshirts()
#     elif "women t-shirts" in user_lower:
#         bot_response = scrape_wix_women_tshirts()
#     elif "sweatshirts" in user_lower or "hoodies" in user_lower:
#         bot_response = scrape_wix_sweatshirts()
#     elif any(word in user_lower for word in ["offer", "offers", "deal", "discount", "sale"]):
#         bot_response = scrape_wix_offers()
#     elif any(word in user_lower for word in ["design lab", "lab design", "custom design"]):
#         bot_response = scrape_wix_design_lab()
#     elif any(word in user_lower for word in ["blog", "articles", "posts"]):
#         bot_response = scrape_wix_blog()
#     elif any(word in user_lower for word in ["contact", "address", "office", "email", "phone", "call", "reach out"]):
#         bot_response = get_chatbot_response(user_message)
#     else:
#         bot_response = get_llm_response(messages[session_id])
#     # --------------------------------------------------------

#     # Store assistant response
#     messages[session_id].append({
#         "role": "assistant",
#         "content": bot_response,
#         "timestamp": datetime.now().isoformat()
#     })

#     cleanup_old_sessions()

#     return Response({
#         "session_id": session_id,
#         "is_new_session": is_new_session,
#         "response": bot_response,
#         "messages": messages[session_id]
#     })


# # -------------------- Contact Response --------------------
# def get_chatbot_response(user_input: str) -> str:
#     query = user_input.lower()
#     contact_keywords = ["contact", "address", "office", "email", "phone", "call", "reach out"]

#     if any(word in query for word in contact_keywords):
#         return (
#             "📞 **Reach Out – We will get back to you**\n\n"
#             "**KARNAMAA Bengaluru Office**\n\n"
#             "📍 NO: 677, 1st Floor, Suit # 221, 27th Main, 13th Cross, Sector 1, "
#             "HSR Layout, Bangalore-560102\n\n"
#             "📱 Mob: +91 6363857937\n"
#             "📧 Email: info@Karnamaa.com\n\n"
#             "👉 [Click here to Contact Us](https://palpurna55.wixsite.com/karnamaa1/contact)"
#         )

#     return "I’m here to help! Please tell me what you’d like to know."


# # -------------------- LLM Fallback --------------------
# def get_llm_response(conversation_history):
#     messages_payload = [
#         {"role": msg['role'], "content": msg['content']}
#         for msg in conversation_history
#     ]
#     try:
#         response = client.chat.completions.create(
#             model="deepseek/deepseek-chat",
#             messages=messages_payload,
#             temperature=0.7,
#             max_tokens=300
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         if "402" in str(e) or "Insufficient Balance" in str(e):
#             try:
#                 response = client.chat.completions.create(
#                     model="openai/gpt-3.5-turbo",
#                     messages=messages_payload,
#                     temperature=0.7,
#                     max_tokens=300
#                 )
#                 return response.choices[0].message.content.strip()
#             except Exception as inner_e:
#                 return f"⚠️ Both DeepSeek and GPT-3.5 failed: {str(inner_e)}"
#         return f"⚠️ LLM API call failed: {str(e)}"


# # -------------------- Cleanup Old Sessions --------------------
# def cleanup_old_sessions():
#     current_time = datetime.now()
#     expired = [
#         sid for sid, data in sessions.items()
#         if current_time - data["last_activity"] > timedelta(hours=SESSION_TTL_HOURS)
#     ]
#     for sid in expired:
#         sessions.pop(sid, None)
#         messages.pop(sid, None)


# # -------------------- Wix Scraper Helpers --------------------
# def scrape_wix_plain_tshirts():
#     url = "https://palpurna55.wixsite.com/karnamaa1/plain-t-shirts-for-men"
#     return scrape_wix_generic(url)

# def scrape_wix_women_tshirts():
#     url = "https://palpurna55.wixsite.com/karnamaa1/women-t-shirts"
#     return scrape_wix_generic(url)

# def scrape_wix_sweatshirts():
#     url = "https://palpurna55.wixsite.com/karnamaa1/sweatshirts-hoodies"
#     return scrape_wix_generic(url)

# def scrape_wix_offers():
#     url = "https://palpurna55.wixsite.com/karnamaa1/offers"
#     return scrape_wix_generic(url)

# def scrape_wix_design_lab():
#     url = "https://palpurna55.wixsite.com/karnamaa1/design-lab"
#     return scrape_wix_generic(url)

# def scrape_wix_blog():
#     url = "https://palpurna55.wixsite.com/karnamaa1/blog"
#     return scrape_wix_generic(url)

# def scrape_wix_graphic_tshirts():
#     url = "https://palpurna55.wixsite.com/karnamaa1/graphic-t-shirts-for-men"
#     items = []

#     from playwright.sync_api import sync_playwright

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url, timeout=60000)

#         page.wait_for_selector('[data-hook="product-item-name-and-price-layout"]', timeout=30000)
#         product_elements = page.query_selector_all('[data-hook="product-item-name-and-price-layout"]')

#         for el in product_elements:
#             try:
#                 name_el = el.query_selector('[data-hook="product-item-name"]')
#                 name = name_el.inner_text().strip() if name_el else "N/A"

#                 price_before = el.query_selector('[data-hook="product-item-price-before-discount"]')
#                 regular_price = price_before.inner_text().strip() if price_before else "N/A"

#                 price_sale = el.query_selector('[data-hook="product-item-price-to-pay"]')
#                 sale_price = price_sale.inner_text().strip() if price_sale else "N/A"

#                 img_el = el.query_selector("img")
#                 img_url = img_el.get_attribute("src") if img_el else ""

#                 link_el = el.query_selector("a")
#                 product_url = link_el.get_attribute("href") if link_el else url

#                 items.append({
#                     "name": name,
#                     "regular_price": regular_price,
#                     "sale_price": sale_price,
#                     "image": img_url,
#                     "url": product_url
#                 })
#             except Exception as e:
#                 print("Error scraping:", e)
#                 continue

#         browser.close()
#     return items

# def scrape_wix_generic(url):
#     items = []
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url, timeout=60000)

#         # Wait for product/blog elements
#         try:
#             page.wait_for_selector('[data-hook="product-item-name-and-price-layout"], [data-hook="blog-item"]', timeout=30000)
#         except:
#             pass

#         # Try scraping product/blog items
#         product_elements = page.query_selector_all('[data-hook="product-item-name-and-price-layout"], [data-hook="blog-item"]')

#         for el in product_elements:
#             try:
#                 name_el = el.query_selector('[data-hook="product-item-name"], [data-hook="blog-item-title"]')
#                 name = name_el.inner_text().strip() if name_el else "N/A"

#                 price_before = el.query_selector('[data-hook="product-item-price-before-discount"]')
#                 regular_price = price_before.inner_text().strip() if price_before else "N/A"

#                 price_sale = el.query_selector('[data-hook="product-item-price-to-pay"]')
#                 sale_price = price_sale.inner_text().strip() if price_sale else "N/A"

#                 img_el = el.query_selector("img")
#                 img_url = img_el.get_attribute("src") if img_el else ""

#                 link_el = el.query_selector("a")
#                 item_url = link_el.get_attribute("href") if link_el else url

#                 items.append({
#                     "name": name,
#                     "regular_price": regular_price,
#                     "sale_price": sale_price,
#                     "image": img_url,
#                     "url": item_url
#                 })
#             except Exception as e:
#                 print("Error scraping item:", e)
#                 continue
#         browser.close()
#     return items

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from datetime import datetime, timedelta
from openai import OpenAI
from playwright.sync_api import sync_playwright

# -------------------- LLM Client --------------------
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# -------------------- Session storage --------------------
sessions = {}
messages = {}
SESSION_TTL_HOURS = 24

# -------------------- Views --------------------
def home(request):
    return render(request, "chatbot/index.html")


@api_view(["POST"])
def chat(request):
    data = request.data
    session_id = data.get("session_id")
    user_message = data.get("message", "").strip()
    current_time = datetime.now()

    # Session handling
    is_new_session = False
    if not session_id or session_id not in sessions:
        session_id = str(current_time.timestamp())
        is_new_session = True
        sessions[session_id] = {"created_at": current_time, "last_activity": current_time}
        messages[session_id] = []
    else:
        sessions[session_id]["last_activity"] = current_time

    # Store user message
    messages[session_id].append({
        "role": "user",
        "content": user_message,
        "timestamp": current_time.isoformat()
    })

    # -------------------- Chatbot Logic --------------------
    user_lower = user_message.lower()
    if "plain t-shirts" in user_lower:
        bot_response = scrape_wix_plain_tshirts()
    elif "women t-shirts" in user_lower:
        bot_response = scrape_wix_women_tshirts()
    elif "graphic t-shirts" in user_lower:
        bot_response = scrape_wix_graphic_tshirts()
    elif "sweatshirts" in user_lower or "hoodies" in user_lower:
        bot_response = scrape_wix_sweatshirts()
    elif any(word in user_lower for word in ["offer", "offers", "deal", "discount", "sale"]):
        bot_response = scrape_wix_offers()
    elif any(word in user_lower for word in ["design lab", "lab design", "custom design"]):
        bot_response = scrape_wix_design_lab()
    elif any(word in user_lower for word in ["blog", "articles", "posts"]):
        bot_response = scrape_wix_blog()
    elif any(word in user_lower for word in ["contact", "address", "office", "email", "phone", "call", "reach out"]):
        bot_response = get_chatbot_response(user_message)
    else:
        bot_response = get_llm_response(messages[session_id])
    # --------------------------------------------------------

    # Store assistant response
    messages[session_id].append({
        "role": "assistant",
        "content": bot_response,
        "timestamp": datetime.now().isoformat()
    })

    cleanup_old_sessions()

    return Response({
        "session_id": session_id,
        "is_new_session": is_new_session,
        "response": bot_response,
        "messages": messages[session_id]
    })


# -------------------- Contact Response --------------------
def get_chatbot_response(user_input: str) -> str:
    query = user_input.lower()
    contact_keywords = ["contact", "address", "office", "email", "phone", "call", "reach out"]

    if any(word in query for word in contact_keywords):
        return (
            "📞 **Reach Out – We will get back to you**\n\n"
            "**KARNAMAA Bengaluru Office**\n\n"
            "📍 NO: 677, 1st Floor, Suit # 221, 27th Main, 13th Cross, Sector 1, "
            "HSR Layout, Bangalore-560102\n\n"
            "📱 Mob: +91 6363857937\n"
            "📧 Email: info@Karnamaa.com\n\n"
            "👉 [Click here to Contact Us](https://palpurna55.wixsite.com/karnamaa1/contact)"
        )
    return "I’m here to help! Please tell me what you’d like to know."


# -------------------- LLM Fallback --------------------
def get_llm_response(conversation_history):
    messages_payload = [{"role": msg['role'], "content": msg['content']} for msg in conversation_history]
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=messages_payload,
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        if "402" in str(e) or "Insufficient Balance" in str(e):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=messages_payload,
                    temperature=0.7,
                    max_tokens=300
                )
                return response.choices[0].message.content.strip()
            except Exception as inner_e:
                return f"⚠️ Both DeepSeek and GPT-3.5 failed: {str(inner_e)}"
        return f"⚠️ LLM API call failed: {str(e)}"


# -------------------- Cleanup Old Sessions --------------------
def cleanup_old_sessions():
    current_time = datetime.now()
    expired = [sid for sid, data in sessions.items() if current_time - data["last_activity"] > timedelta(hours=SESSION_TTL_HOURS)]
    for sid in expired:
        sessions.pop(sid, None)
        messages.pop(sid, None)


# -------------------- Wix Scraper Helpers --------------------
def scrape_wix_plain_tshirts():
    url = "https://palpurna55.wixsite.com/karnamaa1/plain-t-shirts-for-men"
    return scrape_wix_generic(url)

def scrape_wix_women_tshirts():
    url = "https://palpurna55.wixsite.com/karnamaa1/women-t-shirts"
    return scrape_wix_generic(url)

def scrape_wix_graphic_tshirts():
    url = "https://palpurna55.wixsite.com/karnamaa1/graphic-t-shirts-for-men"
    return scrape_wix_generic(url)

def scrape_wix_sweatshirts():
    url = "https://palpurna55.wixsite.com/karnamaa1/sweatshirts-hoodies"
    return scrape_wix_generic(url)

def scrape_wix_offers():
    url = "https://palpurna55.wixsite.com/karnamaa1/offers"
    return scrape_wix_generic(url)

def scrape_wix_design_lab():
    url = "https://palpurna55.wixsite.com/karnamaa1/design-lab"
    return scrape_wix_generic(url)

def scrape_wix_blog():
    url = "https://palpurna55.wixsite.com/karnamaa1/blog"
    return scrape_wix_generic(url)


# -------------------- Generic Wix Scraper --------------------
def scrape_wix_generic(url):
    items = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Wait for product/blog elements
        try:
            page.wait_for_selector('[data-hook="product-item-name-and-price-layout"], [data-hook="blog-item"]', timeout=30000)
        except:
            pass

        # Scrape products/blogs
        product_elements = page.query_selector_all('[data-hook="product-item-name-and-price-layout"], [data-hook="blog-item"]')

        for el in product_elements:
            try:
                name_el = el.query_selector('[data-hook="product-item-name"], [data-hook="blog-item-title"]')
                name = name_el.inner_text().strip() if name_el else "N/A"

                price_before = el.query_selector('[data-hook="product-item-price-before-discount"]')
                regular_price = price_before.inner_text().strip() if price_before else "N/A"

                price_sale = el.query_selector('[data-hook="product-item-price-to-pay"]')
                sale_price = price_sale.inner_text().strip() if price_sale else "N/A"

                img_el = el.query_selector("img")
                img_url = img_el.get_attribute("src") if img_el else ""

                link_el = el.query_selector("a")
                item_url = link_el.get_attribute("href") if link_el else url

                items.append({
                    "name": name,
                    "regular_price": regular_price,
                    "sale_price": sale_price,
                    "image": img_url,
                    "url": item_url
                })
            except Exception as e:
                print("Error scraping item:", e)
                continue
        browser.close()
    return items












