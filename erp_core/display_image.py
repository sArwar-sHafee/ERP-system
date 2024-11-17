from erp_core.node_builder import graph

try:
    image_path = "output_image.png"
    # Get the image bytes
    image_data = graph.get_graph(xray=True).draw_mermaid_png()
    
    # Save bytes to file
    with open(image_path, 'wb') as f:
        f.write(image_data)
    
    print(f"Image saved at {image_path}")
except Exception as e:
    print(f"An error occurred: {e}")
