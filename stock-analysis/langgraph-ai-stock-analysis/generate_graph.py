from IPython.display import display, Image
from langgraph.graph.graph import CompiledGraph

def generate(graph: CompiledGraph):
    try:
        # Assuming graph.get_graph().draw_mermaid_png() generates an image in bytes
        img_data = graph.get_graph().draw_mermaid_png()
        
        # Save the image to disk
        with open("graph.png", "wb") as f:
            f.write(img_data)
        
        print("Image saved as 'graph.png'")
        
        # Display the image
        display(Image(data=img_data))
    except Exception as e:
        print("Failed to process the image. Error:", e)