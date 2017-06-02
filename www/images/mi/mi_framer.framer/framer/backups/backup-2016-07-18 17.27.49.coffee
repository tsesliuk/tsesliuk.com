# Create a PageComponent 
page = new PageComponent
    width: Screen.width
    height: Screen.height
 
pageA = new Layer
    width: page.width
    height: page.height
    parent: page.content
    backgroundColor: "#28affa"
 
pageB = new Layer
    width: page.width
    height: page.height
    backgroundColor: "#90D7FF"
    
pageC = new Layer
    width: page.width
    height: page.height
    backgroundColor: "#37809F" 
    
pageC = new Layer
    width: page.width
    height: page.height
    backgroundColor: "#37809F" 
    
pageC = new Layer
    width: page.width
    height: page.height
    backgroundColor: "#37809F"            
 
page.addPage(pageB, "right")
page.addPage(pageC, "right")
	
		


    

    
 