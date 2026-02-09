"""
Example client script to test the API
"""
import requests
import json
import sys


def process_video(youtube_url: str, api_url: str = "http://localhost:8000"):
    """
    Send a YouTube URL to the API and get learning materials
    
    Args:
        youtube_url: YouTube video URL
        api_url: API base URL (default: http://localhost:8000)
    """
    endpoint = f"{api_url}/process-video"
    
    print(f"🎥 Processing: {youtube_url}")
    print(f"📡 Sending request to: {endpoint}\n")
    
    try:
        response = requests.post(
            endpoint,
            json={"youtube_url": youtube_url},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!\n")
            print("=" * 60)
            print(f"📺 Video: {data['video_title']}")
            print(f"⏱️  Duration: {data['duration']}")
            print("=" * 60)
            
            print("\n📝 SUMMARY:")
            print("-" * 60)
            print(data['summary'])
            
            print("\n\n💡 KEY POINTS:")
            print("-" * 60)
            for i, point in enumerate(data['key_points'], 1):
                print(f"{i}. {point}")
            
            print("\n\n❓ QUIZ QUESTIONS:")
            print("-" * 60)
            for i, q in enumerate(data['quiz'], 1):
                print(f"\nQ{i}: {q['question']}")
                for j, option in enumerate(q['options'], 1):
                    marker = "✓" if option == q['correct_answer'] else " "
                    print(f"  {marker} {j}. {option}")
            
            print("\n" + "=" * 60)
            print("✨ Processing complete!")
            
            # Optionally save to file
            save_to_file = input("\n💾 Save results to file? (y/n): ").lower()
            if save_to_file == 'y':
                filename = "learning_materials.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"✅ Saved to {filename}")
        
        elif response.status_code == 404:
            print("❌ ERROR: Transcript not available")
            print("This video may not have captions/subtitles.")
        
        elif response.status_code == 413:
            print("❌ ERROR: Video too long")
            print("Please try a shorter video (under 60 minutes).")
        
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(response.json().get('detail', 'Unknown error'))
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API")
        print("Make sure the server is running: uvicorn main:app --reload")
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


def main():
    """Main function to run the example"""
    if len(sys.argv) < 2:
        print("🎓 Smart Video Learning Tool - Client Example\n")
        print("Usage:")
        print(f"  python {sys.argv[0]} <youtube_url> [api_url]\n")
        print("Examples:")
        print(f"  python {sys.argv[0]} https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print(f"  python {sys.argv[0]} https://youtu.be/dQw4w9WgXcQ http://localhost:8000")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    api_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000"
    
    process_video(youtube_url, api_url)


if __name__ == "__main__":
    main()
