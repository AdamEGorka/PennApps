import visualizer as gv
import time

def main():
    # Add your code here
    print("Starting the main function")
    
    # Example: Printing numbers from 1 to 10
    
    
    
    gv.add_node()
    gv.add_node()
    gv.add_node()
    gv.add_connection(0, 1)
    
    gv.visualizer()
    
    gv.add_node()
    gv.apply_events()
    
    for i in range(10):
        time.sleep(1)
        
    
# Main
if __name__ == "__main__":
    main()