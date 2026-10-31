"""Main script to generate LangChain and AI Agent blog posts automatically from trending Google News topics"""
import os
import sys
import time
import datetime

# Ensure scripts dir is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all modules
from config import *
from google_news_fetcher import GoogleNewsFetcher
from article_generator import generate_article, generate_image_prompt, generate_stock_photo_keywords
from image_generator import generate_image_featured
from insert_ads import insert_ads_into_content
from google_indexing import submit_to_google_indexing
from google_sheets_logger import log_to_google_sheets
from webpushr_notifier import send_blog_post_notification


def main():
    print("=" * 60)
    print("🚀 Starting AI Blog Generator - Google News Trending Mode")
    print("=" * 60)

    # Verify environment variables
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found in environment")
        return
    print("✅ GEMINI_API_KEY found")

    if PEXELS_API_KEY:
        print("✅ PEXELS_API_KEY configured (Commercial Stock Photos)")
    if UNSPLASH_ACCESS_KEY:
        print("✅ UNSPLASH_ACCESS_KEY configured (Commercial Stock Photos)")
    if POLLINATIONS_API_KEY:
        masked_p_key = f"{POLLINATIONS_API_KEY[:7]}...{POLLINATIONS_API_KEY[-4:]}"
        print(f"✅ POLLINATIONS_API_KEY configured ({masked_p_key})")
    if FREEPIK_API_KEY:
        print("✅ FREEPIK_API_KEY found")

    print(f"\n📊 Posts to generate this run: {POSTS_PER_RUN}")

    # Initialize Google News fetcher and existing post deduplicator
    news_fetcher = GoogleNewsFetcher()

    posts_generated = 0

    for post_num in range(1, POSTS_PER_RUN + 1):
        print(f"\n{'=' * 60}")
        print(f"📝 Processing Post {post_num}/{POSTS_PER_RUN}")
        print("=" * 60)

        # Fetch trending topic from Google News
        print("\n🔥 Fetching trending LangChain / AI Agent topic from Google News...")
        keyword_data = news_fetcher.get_trending_topic_for_blog()

        if not keyword_data:
            print("❌ Failed to fetch trending topic")
            continue

        title = keyword_data['title']
        focus_kw = keyword_data['focus_kw']
        permalink = keyword_data['permalink']
        semantic_kw = keyword_data.get('semantic_kw', '')
        affiliate_links = keyword_data.get('affiliate_links', '')
        hook_kw = keyword_data.get('hook_kw', '')
        search_kw = keyword_data.get('search_kw', '')
        tags = keyword_data.get('tags', '')
        source_link = keyword_data.get('source_link', '')

        print(f"\n✅ Topic selected: {title}")
        print(f"   Focus Keyword: {focus_kw}")
        print(f"   Permalink: {permalink}")
        if source_link:
            print(f"   Source: {source_link}")

        # Setup file paths
        today = datetime.date.today().isoformat()
        post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
        image_file = f"{IMAGES_DIR}/{permalink}.webp"

        # Check if post already exists
        if os.path.exists(post_path):
            print(f"\n⚠️ Post already exists: {post_path}")
            print("   This topic may have already been covered, trying next...")
            continue

        try:
            # Step 1: Generate article
            print(f"\n{'=' * 60}")
            print("Step 1: Generating SEO Article with Gemini AI")
            print("=" * 60)
            if source_link:
                print(f"📰 Source: {source_link}")

            article = generate_article(
                title=title,
                focus_kw=focus_kw,
                permalink=permalink,
                semantic_kw=semantic_kw,
                affiliate_links=affiliate_links,
                hook_kw=hook_kw,
                search_kw=search_kw,
                tags=tags
            )
            print(f"✅ Article generated ({len(article)} characters)")

            # Step 2: Generate featured image prompt and stock search queries
            print(f"\n{'=' * 60}")
            print("Step 2: Preparing Featured Image Prompt & Stock Queries")
            print("=" * 60)
            stock_keywords = generate_stock_photo_keywords(title, focus_kw)
            image_prompt = generate_image_prompt(title, focus_kw)
            print(f"🔍 Stock Queries: {stock_keywords}")
            print(f"📝 AI Prompt: {image_prompt[:120]}...")

            # Step 3: Retrieve or generate and compress featured image
            print(f"\n{'=' * 60}")
            print("Step 3: Retrieving/Generating Featured Image (Pexels/Unsplash/AI)")
            print("=" * 60)
            try:
                generate_image_featured(prompt=image_prompt, output_path=image_file, keywords=stock_keywords)
                print(f"✅ Featured image ready: {image_file}")
            except Exception as img_err:
                print(f"❌ Image creation failed: {img_err}")
                print("⚠️ Skipping this post - will try a different topic next run")
                import traceback
                traceback.print_exc()
                continue

            # Step 4: Insert AdSense in-article ads and save post
            print(f"\n{'=' * 60}")
            print("Step 4: Inserting Ads & Saving Post")
            print("=" * 60)
            final_article = insert_ads_into_content(article)

            with open(post_path, "w", encoding="utf-8") as f:
                f.write(final_article)
            print(f"✅ Post saved (with ads): {post_path}")

            post_url = f"{SITE_DOMAIN}/{permalink}"

            print(f"\n{'=' * 60}")
            print(f"✅ SUCCESS! Post {post_num} Generated")
            print("=" * 60)
            print(f"📰 Title: {title}")
            print(f"🌐 URL: {post_url}")
            if source_link:
                print(f"📰 Source: {source_link}")

            posts_generated += 1

            # Step 5: Post-publish integrations (Push Notifications, Indexing, Sheets)
            if post_num == POSTS_PER_RUN or post_num == posts_generated:
                # Step 5a: Push Notification
                print(f"\n{'=' * 60}")
                print("Step 5a: Sending Push Notification")
                print("=" * 60)
                try:
                    send_blog_post_notification(title, permalink, focus_kw)
                    print("✅ Push notification sent")
                except Exception as e:
                    print(f"⚠️ Push notification skipped/failed: {e}")

                # Step 5b: Google Indexing
                indexing_status = "Not Attempted"
                try:
                    if GOOGLE_SERVICE_ACCOUNT_JSON:
                        print(f"\n{'=' * 60}")
                        print("Step 5b: Submitting to Google Indexing")
                        print("=" * 60)
                        success = submit_to_google_indexing(post_url)
                        indexing_status = "Success" if success else "Failed"
                        print(f"✅ Google Indexing status: {indexing_status}")
                except Exception as e:
                    indexing_status = f"Failed - {str(e)[:50]}"
                    print(f"⚠️ Google Indexing API skipped/failed: {e}")

                # Step 5c: Google Sheets Logger
                try:
                    if GOOGLE_SERVICE_ACCOUNT_JSON and GOOGLE_SPREADSHEET_ID:
                        print(f"\n{'=' * 60}")
                        print("Step 5c: Logging to Google Sheets")
                        print("=" * 60)
                        log_to_google_sheets(
                            title, focus_kw, permalink,
                            image_file, final_article, indexing_status
                        )
                        print("✅ Logged to Google Sheets")
                except Exception as e:
                    print(f"⚠️ Sheets logger skipped/failed: {e}")

            print(f"\n{'=' * 60}")
            print("✅ Post Complete!")
            print("=" * 60)

        except Exception as e:
            print(f"\n{'=' * 60}")
            print(f"❌ FAILED: {e}")
            print("=" * 60)
            print("⚠️ Will try a different topic next run")
            import traceback
            traceback.print_exc()
            continue

    # Final summary
    print(f"\n{'=' * 60}")
    print("🎉 WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"✅ Posts generated: {posts_generated}")
    print(f"📰 Source: Google News (Trending Topics)")

    if posts_generated == 0:
        print("\n⚠️ No posts were generated this run")
        print("💡 Check the logs above for errors")


if __name__ == "__main__":
    main()
