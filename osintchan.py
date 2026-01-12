#!/usr/bin/env python3
"""
OSINTChan - 4chan/8kun OSINT Collection Tool
Searches and archives threads from imageboards for investigation purposes
"""

import requests
import argparse
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

class OSINTChan:
    def __init__(self):
        # 4chan API endpoints - No API key required
        self.fourchan_api = "https://a.4cdn.org"
        self.fourchan_boards = "https://a.4cdn.org/boards.json"
        self.fourchan_images = "https://i.4cdn.org"
        
        # 8kun API endpoints - No API key required
        self.eightkun_api = "https://8kun.top"
        
        self.results = {}
        
    def get_boards(self, site: str = "4chan") -> Dict:
        """Get list of available boards"""
        print(f"[*] Fetching boards from {site}...")
        
        try:
            if site == "4chan":
                response = requests.get(self.fourchan_boards, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    boards = []
                    for board in data.get("boards", []):
                        boards.append({
                            "board": board.get("board"),
                            "title": board.get("title"),
                            "meta_description": board.get("meta_description"),
                            "is_archived": board.get("is_archived", 0)
                        })
                    return {
                        "site": site,
                        "boards_found": len(boards),
                        "boards": boards
                    }
                else:
                    return {"error": f"{site} API error: {response.status_code}"}
            else:
                return {"error": f"Site {site} not yet implemented"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_catalog(self, board: str, site: str = "4chan") -> Dict:
        """Get catalog of threads for a board"""
        print(f"[*] Fetching catalog for /{board}/ on {site}...")
        
        try:
            if site == "4chan":
                url = f"{self.fourchan_api}/{board}/catalog.json"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    threads = []
                    
                    for page in data:
                        for thread in page.get("threads", []):
                            threads.append({
                                "no": thread.get("no"),
                                "subject": thread.get("sub", "No subject"),
                                "comment": thread.get("com", "")[:200],  # First 200 chars
                                "name": thread.get("name", "Anonymous"),
                                "time": thread.get("time"),
                                "replies": thread.get("replies", 0),
                                "images": thread.get("images", 0),
                                "sticky": thread.get("sticky", 0),
                                "closed": thread.get("closed", 0)
                            })
                    
                    return {
                        "site": site,
                        "board": board,
                        "threads_found": len(threads),
                        "threads": threads
                    }
                else:
                    return {"error": f"{site} API error: {response.status_code}"}
            else:
                return {"error": f"Site {site} not yet implemented"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_thread(self, board: str, thread_no: int, site: str = "4chan") -> Dict:
        """Get full thread with all posts"""
        print(f"[*] Fetching thread /{board}/{thread_no} from {site}...")
        
        try:
            if site == "4chan":
                url = f"{self.fourchan_api}/{board}/thread/{thread_no}.json"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    posts = []
                    
                    for post in data.get("posts", []):
                        post_data = {
                            "no": post.get("no"),
                            "time": post.get("time"),
                            "name": post.get("name", "Anonymous"),
                            "subject": post.get("sub", ""),
                            "comment": post.get("com", ""),
                            "trip": post.get("trip", ""),
                            "id": post.get("id", ""),
                            "capcode": post.get("capcode", "")
                        }
                        
                        # Add image info if present
                        if post.get("filename"):
                            post_data["image"] = {
                                "filename": post.get("filename"),
                                "ext": post.get("ext"),
                                "tim": post.get("tim"),
                                "md5": post.get("md5"),
                                "size": post.get("fsize"),
                                "image_url": f"{self.fourchan_images}/{board}/{post.get('tim')}{post.get('ext')}"
                            }
                        
                        posts.append(post_data)
                    
                    return {
                        "site": site,
                        "board": board,
                        "thread_no": thread_no,
                        "posts_found": len(posts),
                        "posts": posts,
                        "thread_url": f"https://boards.4chan.org/{board}/thread/{thread_no}"
                    }
                elif response.status_code == 404:
                    return {
                        "error": "Thread not found (404) - may have been deleted or archived"
                    }
                else:
                    return {"error": f"{site} API error: {response.status_code}"}
            else:
                return {"error": f"Site {site} not yet implemented"}
        except Exception as e:
            return {"error": str(e)}
    
    def search_catalog(self, board: str, keyword: str, site: str = "4chan") -> Dict:
        """Search catalog for threads containing keyword"""
        print(f"[*] Searching /{board}/ for '{keyword}' on {site}...")
        
        catalog = self.get_catalog(board, site)
        
        if "error" in catalog:
            return catalog
        
        keyword_lower = keyword.lower()
        matching_threads = []
        
        for thread in catalog.get("threads", []):
            subject = thread.get("subject", "").lower()
            comment = thread.get("comment", "").lower()
            
            if keyword_lower in subject or keyword_lower in comment:
                matching_threads.append(thread)
        
        return {
            "site": site,
            "board": board,
            "keyword": keyword,
            "matches_found": len(matching_threads),
            "threads": matching_threads
        }
    
    def get_archived_threads(self, board: str, site: str = "4chan") -> Dict:
        """Get list of archived threads"""
        print(f"[*] Fetching archived threads for /{board}/ on {site}...")
        
        try:
            if site == "4chan":
                url = f"{self.fourchan_api}/{board}/archive.json"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    archived = response.json()
                    return {
                        "site": site,
                        "board": board,
                        "archived_threads": len(archived),
                        "thread_ids": archived[:100]  # First 100
                    }
                else:
                    return {"error": f"{site} API error: {response.status_code}"}
            else:
                return {"error": f"Site {site} not yet implemented"}
        except Exception as e:
            return {"error": str(e)}
    
    def run_investigation(self, board: str, operation: str, **kwargs) -> Dict:
        """Run investigation operation"""
        print(f"\n[+] Starting OSINTChan investigation")
        print(f"[+] Board: /{board}/")
        print(f"[+] Operation: {operation}")
        print(f"[+] Timestamp: {datetime.now().isoformat()}\n")
        
        site = kwargs.get("site", "4chan")
        
        results = {
            "board": board,
            "operation": operation,
            "site": site,
            "timestamp": datetime.now().isoformat()
        }
        
        if operation == "catalog":
            results["data"] = self.get_catalog(board, site)
        
        elif operation == "thread":
            thread_no = kwargs.get("thread_no")
            if not thread_no:
                results["error"] = "Thread number required for thread operation"
            else:
                results["data"] = self.get_thread(board, thread_no, site)
        
        elif operation == "search":
            keyword = kwargs.get("keyword")
            if not keyword:
                results["error"] = "Keyword required for search operation"
            else:
                results["data"] = self.search_catalog(board, keyword, site)
        
        elif operation == "archive":
            results["data"] = self.get_archived_threads(board, site)
        
        elif operation == "boards":
            results["data"] = self.get_boards(site)
        
        else:
            results["error"] = f"Unknown operation: {operation}"
        
        return results
    
    def save_results(self, results: Dict, output_file: str):
        """Save results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n[+] Results saved to: {output_file}")
    
    def print_results(self, results: Dict):
        """Print results to console"""
        print("\n" + "="*60)
        print("OSINTCHAN INVESTIGATION RESULTS")
        print("="*60)
        print(f"Board: /{results.get('board', 'N/A')}/")
        print(f"Operation: {results.get('operation')}")
        print(f"Site: {results.get('site')}")
        print(f"Timestamp: {results.get('timestamp')}")
        print("="*60)
        
        data = results.get("data", {})
        
        if "error" in results:
            print(f"\nError: {results['error']}")
        elif "error" in data:
            print(f"\nError: {data['error']}")
        else:
            operation = results.get("operation")
            
            if operation == "catalog":
                threads = data.get("threads", [])
                print(f"\nThreads found: {len(threads)}")
                print("\nRecent threads:")
                for thread in threads[:10]:
                    print(f"\n  Thread #{thread['no']}")
                    print(f"  Subject: {thread['subject']}")
                    print(f"  Replies: {thread['replies']} | Images: {thread['images']}")
                    if thread.get('sticky'):
                        print(f"  [STICKY]")
            
            elif operation == "thread":
                posts = data.get("posts", [])
                print(f"\nPosts found: {len(posts)}")
                print(f"Thread URL: {data.get('thread_url')}")
                print("\nFirst post:")
                if posts:
                    op = posts[0]
                    print(f"  #{op['no']} - {op['name']} - {op['time']}")
                    print(f"  Subject: {op['subject']}")
                    print(f"  Comment: {op['comment'][:200]}")
            
            elif operation == "search":
                matches = data.get("matches_found", 0)
                print(f"\nMatches found: {matches}")
                threads = data.get("threads", [])
                for thread in threads[:10]:
                    print(f"\n  Thread #{thread['no']}")
                    print(f"  Subject: {thread['subject']}")
                    print(f"  Comment: {thread['comment'][:150]}")
            
            elif operation == "archive":
                count = data.get("archived_threads", 0)
                print(f"\nArchived threads: {count}")
            
            elif operation == "boards":
                boards = data.get("boards", [])
                print(f"\nBoards found: {len(boards)}")
                print("\nAvailable boards:")
                for board in boards[:20]:
                    print(f"  /{board['board']}/ - {board['title']}")
        
        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description="OSINTChan - 4chan/8kun OSINT Collection Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  List all boards:
    python osintchan.py -o boards
  
  Get catalog for /pol/:
    python osintchan.py pol -o catalog
  
  Get specific thread:
    python osintchan.py pol -o thread -t 123456789
  
  Search for keyword:
    python osintchan.py pol -o search -k "election"
  
  Get archived threads:
    python osintchan.py pol -o archive
        """
    )
    
    parser.add_argument(
        "board",
        nargs="?",
        help="Board name (e.g., pol, b, int)"
    )
    parser.add_argument(
        "-o", "--operation",
        choices=["catalog", "thread", "search", "archive", "boards"],
        required=True,
        help="Operation to perform"
    )
    parser.add_argument(
        "-t", "--thread",
        type=int,
        help="Thread number (for thread operation)"
    )
    parser.add_argument(
        "-k", "--keyword",
        help="Keyword to search for (for search operation)"
    )
    parser.add_argument(
        "-s", "--site",
        choices=["4chan", "8kun"],
        default="4chan",
        help="Imageboard site (default: 4chan)"
    )
    parser.add_argument(
        "-f", "--output",
        help="Output file for JSON results"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.operation != "boards" and not args.board:
        parser.error("board is required for this operation")
    
    if args.operation == "thread" and not args.thread:
        parser.error("-t/--thread is required for thread operation")
    
    if args.operation == "search" and not args.keyword:
        parser.error("-k/--keyword is required for search operation")
    
    # Run investigation
    osintchan = OSINTChan()
    results = osintchan.run_investigation(
        board=args.board or "",
        operation=args.operation,
        site=args.site,
        thread_no=args.thread,
        keyword=args.keyword
    )
    
    # Print results
    osintchan.print_results(results)
    
    # Save if output file specified
    if args.output:
        osintchan.save_results(results, args.output)

if __name__ == "__main__":
    main()
