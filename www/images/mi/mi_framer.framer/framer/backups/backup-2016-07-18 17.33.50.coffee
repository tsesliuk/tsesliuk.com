# Create a PageComponent 
page = new PageComponent
    width: Screen.width
    height: Screen.height
 
 
 viewA_2x = new Layer
	width: 750
	height: 2824
	image: "images/viewA@2x.png"
 
 
pageA = new Layer
    width: page.width
    height: page.height
    parent: page.content
    backgroundColor: "#28affa"
    
 viewA_2x = new Layer
	width: 750
	height: 2824
	image: "images/viewA@2x.png"   
 
pageB = new Layer
    width: page.width
    height: page.height
    backgroundColor: "#90D7FF"
    backgroundA = new BackgroundLayer
	image: "images/viewA@2x.png"
    
pageC = new Layer
    width: page.width
    height: page.height
    backgroundColor: "#37809F" 
    
pageD = new Layer
    width: page.width
    height: page.height
    backgroundColor: "#37809F" 
    
pageE = new Layer
    width: page.width
    height: page.height
    backgroundColor: "#37809F"           
 
page.addPage(pageB, "right")
page.addPage(pageC, "right")
page.addPage(pageD, "right")
page.addPage(pageE, "right")




	
		


    

    
 