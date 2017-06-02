# Create a PageComponent 
page = new PageComponent
    width: Screen.width
    height: Screen.height
 
pageOne = new Layer
    width: page.width
    height: page.height
    parent: page.content
    backgroundColor: "#28affa"
 
pageTwo = new Layer
    width: page.width
    height: page.height
    backgroundColor: "#90D7FF"
 
page.addPage(pageTwo, "right")
 
# Automatically scroll to pageTwo 
page.snapToPage( pageTwo)
	
		


    

    
 