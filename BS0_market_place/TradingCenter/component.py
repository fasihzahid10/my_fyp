class CardsWithButton:
    def __init__(self, img_url, title, detail, button_url,price,rank,button_tool_tip, button_name):
      black_stars = int(rank*5)
      stars = ""
      for i in range(5):
        if black_stars >= 0:
          stars += "&#9733;"
          black_stars -= 1
        else:
          stars += "&#9734;"        
      self.html = f"""
<div class="card" style="width: 18rem; margin-left: 10px;">
  <img src="{img_url}" class="card-img-top" style="height: 180px;" alt="...">
  <div class="card-body">
    <p class="card-title" style="font-weight:bold">{title}</p>
    <p class="card-text" style="height: 45px; overflow: hidden;">{detail}</p>
    <p class="card-text" style="text-align: center; height:10px;"><small class="text-muted"> {price}</small></p>
    <p class="card-text" style="text-align: center; height:10px;"> {stars}</p>
    <a href="{button_url}" class="btn btn-light border border-dark" data-bs-toggle="tooltip" data-bs-placement="bottom" title="{button_tool_tip}">{button_name}</a>
  </div>
</div>
         """
class CardsWithTwoButton:
    def __init__(self, img_url, title, detail, button_url,button_tool_tip, button_name,button_url_,button_tool_tip_, button_name_):
        self.html = f"""
<div class="card" style="width: 18rem; margin-left: 10px;">
  <img src="{img_url}" class="card-img-top" style="height: 120px;" alt="...">
  <div class="card-body">
    <p class="card-title" style="font-weight:bold">{title}</p>
    <p class="card-text" style="height: 100px; overflow: hidden;">{detail}</p>
    <a href="{button_url}" class="btn btn-light border border-dark" data-bs-toggle="tooltip" data-bs-placement="bottom" title="{button_tool_tip}">{button_name}</a>
    <a href="{button_url_}" class="btn btn-danger" data-bs-toggle="tooltip" data-bs-placement="bottom" title="{button_tool_tip_}">{button_name_}</a>
  </div>
</div>
         """
class RelatedCards:
  def __init__(self,name,objlis):
    cards = ""
    for obj in objlis:
      cards += f"""
      <div style="margin: 3px;">
      {obj.html}
    </div>
      """
    self.html = f"""
    <h1 class="bg-dark border-light" style="text-align: center;color:white;"> {name} </h1>
<div class="bg-dark" style="display: flex;flex-direction: row; flex-wrap: wrap;justify-content: center;">
  {cards}
</div>
    """

class HorizontalImageCard:
    def __init__(self ,img_url, title, detail,price, button_url, button_tool_tip, button_name,update_url = ""):
        if update_url == "":
            update_button = ""
        else:
            update_button = f'<a href="{update_url}" class="btn btn-light border border-dark" style="width:48%;" data-bs-toggle="tooltip" data-bs-placement="bottom" title=" update data ">update </a>'
        self.html = f""" 
        <div class="card mb-3 bg-dark" style="color:white;">
      <div class="row g-0">
        <div class="col-md-4" style = "height: 300px;">
          <img src="{img_url}" style="width: 100%; height: 100%;" alt="...">
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title" style="text-align: center;">{title}</h5>
            <p class="card-text" style="text-align: center;">{detail}</p>
            <p class="card-text" style="text-align: center;"><small class="text-muted">{price}</small></p>
            <a href="{button_url}" class="btn btn-light border border-dark" style="width:48%;"  data-bs-toggle="tooltip" data-bs-placement="bottom" title="{button_tool_tip}">{button_name}</a>
            {update_button}
          </div>
        </div>
      </div>
    </div>
        """
class HorizontalImageCardWidoutButtons:
    def __init__(self ,img_url, title, detail,price):
        self.html = f""" 
    <div class="card mb-3 bg-dark">
      <div class="row g-0">
        <div class="col-md-4" style = "height: 300px;">
          <img src="{img_url}" style="width: 100%; height: 100%;" alt="...">
        </div>
        <div class="col-md-8">
          <div class="card-body" style="color:white;">
            <h5 class="card-title" style="text-align: center;">{title}</h5>
            <p class="card-text" style="text-align: center;">{detail}</p>
            <p class="card-text" style="text-align: center;"><small class="text-muted">{price}</small></p>
          </div>
        </div>
      </div> 
      </div>       
        """
class HorizontalImageCardWithForInventory:
  def __init__(self,img_url, title, detail,price,amount,dir,amo:str):
    if amo:
      if amo.isdigit():
        amo = int(amo)
        if dir == ">>":
          amo += 1
        elif dir == "<<":
          amo -= 1
      else:
        amo = 0
    else:
      amo = 0
    if amo > amount or amo < 0:
        amo = 0
    self.html = f"""
        <div class="card mb-3 bg-dark">
      <div class="row g-0">
        <div class="col-md-4" style = "height: 300px;">
          <img src="{img_url}" style="width: 100%; height: 100%;" alt="...">
        </div>
        <div class="col-md-8" style="color:white">
          <div class="card-body">
            <h5 class="card-title" style="text-align: center;">{title}</h5>
            <p class="card-text" style="text-align: center;">{detail}</p>
            <p class="card-text" style="text-align: center;"><small class="text-muted"> {price}</small></p>
            <div style = "display:flex; flex-direction:row;">
            <form>
              <input type="submit" value="<<" name = "dir" class="btn btn-light border border-dark" style = "height:40px;" />
              <input type = "number" name = "amo" value = {amo} class = "btn btn-light border border-dark" style = "height:40px;"/>
              <input type="submit" value=">>" class="btn btn-light border border-dark" name = "dir" style = "height:40px;"/>
            </form>

            <form style = "margin:2px;">
                <input type="hidden" value="{amo}" name = "amounts">
                <input class="btn btn-light border border-dark" type="submit" value = "Add To Cart">
            </form>
          </div>
        </div>
      </div> 
      </div> 
    """
class HorizontalImageCardWithForSoftware:
  def __init__(self,img_url, title, detail,price):
    self.html = f"""
        <div class="card mb-3 bg-dark" style="color:white;">
      <div class="row g-0">
        <div class="col-md-4" style = "height: 300px;">
          <img src="{img_url}" style="width: 100%; height: 100%;" alt="...">
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title" style="text-align: center;">{title}</h5>
            <p class="card-text" style="text-align: center;">{detail}</p>
            <p class="card-text" style="text-align: center;"><small class="text-muted">{price}</small></p>
            <form>
                <input type="hidden" name="software" value="bought"/>
                <input class="btn btn-light border border-dark" type="submit" value = "Add To Cart">
            </form>
          </div>
        </div>
      </div> 
      </div> 
    """
class SliderCard:
    def __init__(self,img_url, title): 
        self.html = f"""
<div class="card text-black border-light" >
  <img src="{img_url}" class="card-img" style="max-height: 400px;" alt="...">
  <div class="card-img-overlay">
    <h5 class="card-title text-muted">{title}</h5>
  </div>
</div>        
        """

class RemoveBth:
  def __init__(self,url):
    self.html = f"""
      <div class="card">
          <div class="card-body bg-dark" style="height: 10%; width: 99vw; overflow: hidden;">
            <a class = "btn btn-danger" href="{url}"> Remove </a>
          </div>
        </div>
    """

class InfoButtons:
  def __init__(self,name1,name2,value1,value2,url1,url2):
    print(value1,value2)
    val1 = ""
    if value1:
      val1 = f"""
  <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
    {value1}
    <span class="visually-hidden">unread messages</span>
  </span>      
      """
    val2 = ""
    if value2:
      val2 = f"""
  <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
    {value2}
    <span class="visually-hidden">unseen Orders</span>
  </span>      
      """
    self.html = f"""
      <div class="card border border-dark">
          <div class="card-body bg-dark" style="height: 10%; width: 99vw; overflow: hidden;display:flex; flex-direction:row; justify-content:right;">
                <a href="{url1}" class="btn btn-light border border-dark position-relative" style="margin:3px; border-radius:30px;">
                    {name1}
                    {val1}
              </a>
                <a href = "{url2}" class="btn btn-light border border-dark position-relative" style="margin:3px;border-radius:30px;">
                    {name2}
                    {val2}
              </a>
          </div>
        </div>
    """

class LongDescription:
    def __init__(self ,description):
        self.html = f""" 
        <div class="card bg-dark border-light" style="text-align: center; display: flex;justify-content: center;align-items: center;width: 100%;height: 20%;overflow-y:scroll;color:white;">
      <div class="card-body"> {description} </div>
        </div>       
        """

class DropDownButton:
  def __init__(self,links:dict,button_name = "&plus; Add products"):
    link_in_lis = ""
    for name,link in links.items():
      link_in_lis += f'<li><a class="dropdown-item" href="{link}">{name}</a></li>\n'
    self.html = f"""
    <div class="dropdown">
  <a class="btn btn-light border border-dark dropdown-toggle"  href="#" role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
   {button_name}
  </a>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
      {link_in_lis}
  </ul>
</div>
    """

class InformationCard:
  def __init__(self,title,description,profit,allowed,button_url,deliver = False,button_name= "Register Name"):
    self.html = f""" 
   <div class="card text-black bg-light mb-3" style="max-width: 18rem;text-align: center;">
      <div class="card-header">{title}</div>
      <div class="card-body">
      <p class="card-text">{description}</p>
      <p class="card-text"><small>{allowed}</small></p>
      <p class="card-text"><small>{profit}</small></p>
        <p class="card-text"><small>delivery services provided {deliver}</small></p>
      <a class="btn btn-success" href="{button_url}">{button_name}</a>
    </div>
  </div>
    """
class TextBodyCard:
  def __init__(self,body):
    self.html = f"""
    <div class="card bg-dark border-light" style="height: 10%; overflow: hidden;color:white;">
        <div class="card-body">
          {body}
        </div>
    </div>
     """

class HeaderAndFooterCard:
  def __init__(self,title,detail,button_url = "",button_name = 'update'):
    button = ""
    if button_url != "":
      button = f'<a href="{button_url}" class="btn btn-light border border-dark" style="width:30%;"  data-bs-toggle="tooltip" data-bs-placement="bottom" title="update data">{button_name}</a>'
    self.html = f""" 
<div class="card bg-dark border-light" style="color:white;" >
  <div class="card-header" style="text-align:center;">
    {title}
  </div>
  <div class="card-body bg-dark" style="text-align:center; color:white;">
    <p class="card-text" style="height: 100px; overflow-y: scroll;">{detail}</p>
   {button}
  </div>
</div>    
    """
class MessageCard:
  def __init__(self,title,subject,button_url,button_color):
    self.html = f"""
  <div class="card bg-dark border-light" style="text-aligh:center;color:white">
    <h5 class="card-header border-light">{title}</h5>
    <div class="card-body">
      <p class="card-text">{subject}</p>
      <a href="{button_url}" class="btn {button_color}">See Details</a>
    </div>
</div>
    """
class MessageDetailCard:
  def __init__(self,title,subject,detail,to):
    self.html = f"""
  <div class="card bg-dark border-light" style="text-aligh:center;color:white;">
    <h5 class="card-header border-light">from {title}</h5>
    <div class="card-body">
      <h5 class="card-title">{subject}</h5>
      <p class="card-text">{detail}</p>
    </div>
    <div class="card-footer text-muted">
      to  {to}
    </div>
</div>
    """
class CreateMessageButton:
  def __init__(self,button_url,inbox = "",outbox = "",firts_name = "Compose"):
    inb = ""
    outb = ""
    if inbox != "":
      inb = f'<a class="btn btn-outline-primary" style="margin-left: 30px;" href="{inbox}">Inbox</a>'
    if outbox != "":
      outb = f'<a class="btn btn-outline-primary" style="margin-left: 30px;" href="{outbox}">OutBox</a>'
    self.html = f"""
    <div class= "navbar navbar-expand-lg navbar-dark bg-dark" style="color:white">
      <a class="btn btn-outline-primary" style="margin-left: 30px;" href="{button_url}"> {firts_name}</a>
      {inb}
      {outb}
    </div>
    """
class OrdersCardWithTwoButtons:
  def __init__(self,title,type_,first,second,third,first_btn_url,first_btn_name,second_btn_url,second_btn_name):
    self.html = f""" 
          <div class="card" style="width: 18rem; text-align: center;">
            <div class="card-header">
              {title}
             <p> <small class="text-muted">({type_})</small></p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">{first}</li>
              <li class="list-group-item">{second}</li>
              <li class="list-group-item">{third}</li>
              <li class="list-group-item"><a href="{first_btn_url}" style="width: 45%;" class="btn btn-light border border-dark">{first_btn_name}</a><a href="{second_btn_url}" class="btn btn-light border border-dark" style="width: 45%;margin-left: 3px;">{second_btn_name}</a></li>
            </ul>
          </div>    
    """

class OrdersCardWithOneButtons:
  def __init__(self,title,type_,first,second,third,first_btn_url,first_btn_name):
    self.html = f""" 
          <div class="card" style="width: 18rem; text-align: center;">
            <div class="card-header">
              {title}
             <p> <small class="text-muted">({type_})</small></p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">{first}</li>
              <li class="list-group-item">{second}</li>
              <li class="list-group-item">{third}</li>
              <li class="list-group-item"><a href="{first_btn_url}" style="width: 45%;" class="btn btn-light border border-dark">{first_btn_name}</a>
              </li>
            </ul>
          </div>    
    """
class OrdersCardWithOutButtons:
  def __init__(self,title,type_,first,second,third,fourth):
    self.html = f"""
          <div class="card" style="width: 18rem; text-align: center;">
            <div class="card-header">
              {title}
             <p> <small class="text-muted">({type_})</small></p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">{first}</li>
              <li class="list-group-item">{second}</li>
              <li class="list-group-item">{third}</li>
              <li class="list-group-item">{fourth}</li>
            </ul>
          </div>      
    """
class ShowAllOrders:
  def __init__(self,title,submit_button_name,name,value):
     self.html = f"""
            <form style="width:90vw;">
                <h5 style="text-align:center;"> {title} </h5>
                <input type="hidden" name="{name}" value="{value}"/>
                <input class="btn btn-light border border-dark" type="submit" value = "{submit_button_name}">
            </form>
     """

class ShowAdminOrders:
  def __init__(self,title,submit_button_name,name,value):
    self.html = f"""
            <form style="width:90vw;">
                <h5 style="text-align:center;"> {title} </h5>
                <input type="hidden" name="{name}" value="{value}"/>
                <input class="btn btn-light border border-dark" type="submit" value = "{submit_button_name}">
            </form>
     """


class FullWidthTitle:
  def __init__(self,title):
    self.html = f"""
    <div  class="card-header" style="width:90vw";> <p>{title}</p></div>
    """

class FinantialTable:
  def __init__(self,rows):
    row = ""
    for i in rows:
      row += f"""    
    <tr>
      <th scope="col">{i[0]}</th>
      <th scope="col">{i[1]}</th>
      <th scope="col">{i[2]}</th>
      <th scope="col">{i[3]}</th>
      <th scope="col">{i[4]}</th>
    </tr>"""

    self.html = f"""

<table class="table">
  <thead>
    <tr>
      <th scope="col">Date of Order</th>
      <th scope="col">Date of Transection</th>
      <th scope="col">Product</th>
      <th scope="col">Recived</th>
      <th scope="col">Amount Pay</th>
    </tr>
  </thead>
  <tbody>
        {row}
  </tbody>
</table>    
    """

class FinantialTableBalance:
  def __init__(self,current,commited):

    self.html = f"""

<table class="table" style="color:white;">
  <thead>
    <tr>
      <th scope="col">Current Amount</th>
      <th scope="col">Commited Amount</th>
    </tr>
  </thead>
  <tbody>
<tr>
      <th scope="col">{current}</th>
      <th scope="col">{commited}</th>
    </tr>
  </tbody>
</table>    
    """

class CreateFinnantialForm:
  def __init__(self,error = ""):
      self.html = f"""
    <div class= "navbar navbar-expand-lg navbar-dark bg-dark" style="color:white">
    <form>
  <div class="input-group mb-3">
    <span class="input-group-text" id="basic-addon1">MSISD</span>
    <input type="text" name="msid" class="form-control" placeholder="enter easy paisa msisd #" aria-label="Username" aria-describedby="basic-addon1">
</div>
<div class="input-group mb-3 bg-dark border-light">
  <span class="input-group-text">PKR</span>
  <input type="number" name="widthraw_amount" class="form-control" aria-label="Amount">
  <span class="input-group-text">.00</span>
</div>
      <p>{error}</p>
      <input type="submit" class="btn btn-outline-primary" style="margin-left: 30px;" name = "recive_btn" value="Widraw Amount" /> 
    </form>
    </div>
    """


class RanKingCard:
  def __init__(self,total_business,happ,trans):
    
    self.html = f"""
<div class="card border-light bg-dark mb-3" style="width:100%;text-align: center; color:white;">
  <div class="card-header">Rank in Market</div>
  <div class="card-body text-dark">
<table class="table" style = "color:white;">
  <thead>
    <tr>
      <th scope="col">Total Business</th>
      <th scope="col">Successfull</th>
      <th scop="col">Customer happiness</th>
    </tr>
  </thead>
  <tbody>
<tr style="background-color:white;">
    <th scope="col">
      
      <svg id="svg" style="width:150px" viewbox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="#000000"/>
          <!-- first fill,second empty -->
          <path fill="none" stroke-linecap="round" stroke-width="5" stroke="#fff"
              stroke-dasharray="{int(total_business*251)},251"
                d="M50 10
                  a 40 40 0 0 1 0 80
                  a 40 40 0 0 1 0 -80"/>
          <text fill="white" x="50" y="50" text-anchor="middle" dy="7" font-size="20">{int(total_business*100)}%</text>
      </svg>      
      </th>
      <th scope="col">
      <svg id="svg" style="width:150px" viewbox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="#000000"/>
          <!-- first fill,second empty -->
          <path fill="none" stroke-linecap="round" stroke-width="5" stroke="#fff"
              stroke-dasharray="{int(trans*251)},251"
                d="M50 10
                  a 40 40 0 0 1 0 80
                  a 40 40 0 0 1 0 -80"/>
          <text fill="white" x="50" y="50" text-anchor="middle" dy="7" font-size="20">{int(trans*100)}%</text>
      </svg>
      </th>
      <th scope="col">
      <svg id="svg" style="width:150px" viewbox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="#000000"/>
          <!-- first fill,second empty -->
          <path fill="none" stroke-linecap="round" stroke-width="5" stroke="#fff"
              stroke-dasharray="{int(happ*251)},251"
                d="M50 10
                  a 40 40 0 0 1 0 80
                  a 40 40 0 0 1 0 -80"/>
          <text fill="white" x="50" y="50" text-anchor="middle" dy="7" font-size="20">{int(happ*100)}%</text>
      </svg>
      
      
      </th>
    </tr>
  </tbody>
</table>    
  </div>
</div>    
    """

class CommentsCard:
  def __init__(self,sender,rating,message):
      print(rating)
      black_stars = rating
      stars = ""
      for i in range(5):
        if black_stars > 0:
          print("black star")
          stars += "&#9733;"
          black_stars -= 1
        else:
          print("white star")
          stars += "&#9734;"  
      self.html = f"""
<div class="card border-light bg-dark mb-3" style="width:100%; color:white;">
  <div class="card-header" style = "text-align: center;" style = "color:white;">{sender}</div>
  <div class="card-body bg-light">
    <p class="card-text" style="color:black;">{stars}</p>
    <p class="card-text" style = "text-align:center; color:black;" >{message} </p>
  </div>
</div>    
    """

class MlMaxDistance:
  def __init__(self,ran):
    items = f"<option value='0'>Select Min Number</option>"
    for i in range(1,ran+1):
      items += f'<option value="{i}">{i}</option>'
    self.html = f"""
            <form style="width:90vw; color:white">
                 <select name="amounts" id="amount" class="btn btn-light border border-dark">
                    {items}
                </select>
                <input class="btn btn-light border border-dark" type="submit" value = "select">
            </form>

     """
class MLTables:
  def __init__(self,typ,lis):
    items = ""
    for i in lis:
      items += f"""    
    <tr>
      <th scope="col">{typ}</th>
      <th scope="col">{i.first.name}</th>
      <th scope="col">{i.second.name}</th>
    </tr>"""

    self.html = f"""

<table class="table" style="color:white">
  <thead>
    <tr>
      <th scope="col">Type Of Relation</th>
      <th scope="col">First</th>
      <th scope="col">Second</th>
    </tr>
  </thead>
  <tbody>
        {items}
  </tbody>
</table>    
     """


class features_bar:
  def __init__(self,feature):
      self.html = f"""
{feature}
      """

class cust_features:
  def __init__(self,objlis):
    items = ""
    for obj in objlis:
      items += f'<li class="list-group-item bg-dark" style="color:white;">{obj.description}'
      if obj.ref_url:
        items += f'<a href="{obj.ref_url}" class = "btn btn-light border border-dark> Get </a>'
      items += "</li>"

    self.html = f"""
<div class="card bg-dark" style="width: 100%; color:white;">
  <div class="card-header">
    Description
  </div>
  <ul class="list-group list-group-flush">
      {items}
  </ul>
</div>    
    """

class owner_features:
  def __init__(self,objlis,inv_ref,sof_ref,ser_ref):
    items = f'<li class="list-group-item bg-dark" style="color:white;">{add_feature_form(inv_ref,sof_ref,ser_ref).html}</li>'
    for obj in objlis:
      items += f'<li class="list-group-item bg-dark" style="color:white;">{obj.description}'
      items += delete_form(obj.id).html
      if obj.ref_url:
        print(obj.ref_url)
        items += f'<a href="{obj.ref_url}" class = "btn btn-light border border-dark"> Get </a>'
      items += "</li>"


    self.html = f"""
      <div class="card bg-dark" style="width: 100%; color:white">
        <div class="card-header">
          Description
        </div>
        <ul class="list-group list-group-flush">
            {items}
        </ul>
      </div>    
    """



class delete_form:
  def __init__(self,i):
    self.html = f"""
<form>
<input type="hidden" name = "del_fea_btn" value = "{i}" />        
<input class="btn btn-danger" type="submit" value="delete"/>
</form>
    """


class add_feature_form:
  def __init__(self,inv_ref,sof_ref,ser_ref):
    items = f"<option value='-1_none'>select referances</option>"
    for inv_ob in inv_ref:
      items += f"<option value='{inv_ob.pk}_inv'>{inv_ob.name}</option>"

    for sof_ob in sof_ref:
      items += f"<option value='{sof_ob.pk}_sof'>{sof_ob.name}</option>"

    for ser_ob in ser_ref:
      items += f"<option value='{ser_ob.pk}_ser'>{ser_ob.name}</option>"
    self.html = f"""
            <form>
                <input type="text" name="feature" placeholder = "add new feature"  style="width:60%";/>
                 <select name="own_ref" class="btn btn-light border border-dark">
                    {items}
                </select>

                <input class="btn btn-light border border-dark" type="submit" name="insert_btn" value = "insert">
            </form>
     """


class Bill:
  def __init__(self,total_bil,balance,checkout_url):
    have_to_pay = 0
    if balance < total_bil:
      have_to_pay = total_bil - balance
    self.html = f"""
<div class="card bg-dark text-white mb-3" style="width:100vw;text-align:center;">
    <div class="card-header">Summary</div>
    <div class="card-body">
      <h5 class="card-title">Total Bill</h5>
      <table class="table" style="color:white">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Account Name</th>
            <th scope="col">Amount</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">1</th>
            <td>Total Purchase</td>
            <td>{total_bil}PKR</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>Balance Available</td>
            <td>{balance}PKR</td>
          </tr>
          <tr>
            <th scope="row">3</th>
            <td>Have To Pay</td>
            <td>{have_to_pay}PKR</td>
          </tr>
        </tbody>
      </table>
      
      <a class="btn btn-success" href="{checkout_url}">Check Out</a>
    </div>
  </div>      
      """

class Bill_Form:
  def __init__(self,total_bil,balance):
    have_to_pay = 0
    if balance < total_bil:
      have_to_pay = total_bil - balance
    self.html = f"""
<div class="card text-white bg-dark mb-3" style="width:100vw;text-align:center;">
    <div class="card-header">Summary</div>
    <div class="card-body">
      <h5 class="card-title">Total Bill</h5>
      <table class="table" style="color:white;">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Account Name</th>
            <th scope="col">Amount</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">1</th>
            <td>Total Purchase</td>
            <td>{total_bil}PKR</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>Balance Available</td>
            <td>{balance}PKR</td>
          </tr>
          <tr>
            <th scope="row">3</th>
            <td>Have To Pay</td>
            <td>{have_to_pay}PKR</td>
          </tr>
        </tbody>
      </table>
      <form>
        <input type="hidden" name = "check_out_fin" value="checked_click" />
        <input class = "btn btn-light border border-dark" type="submit" value="check out"/>
      </form>
    </div>
  </div>      
      """


class Check_Out_Transfer:
  def __init__(self,dic,home):
    self.html = f"""
<div class="card text-white bg-primary mb-3" style="width:100vw;text-align:center;">
    <div class="card-header">Summary</div>
    <div class="card-body">
      <h5 class="card-title">Total Bill</h5>
      <table class="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Account Name</th>
            <th scope="col">responce</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">1</th>
            <td>Order Id</td>
            <td>{dic["orderId"]}PKR</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>transactionId</td>
            <td>{dic["transactionId"]}PKR</td>
          </tr>
          <tr>
            <th scope="row">3</th>
            <td>transactionDateTime</td>
            <td>{dic["transactionDateTime"]}PKR</td>
          </tr>
          <tr>
            <th scope="row">3</th>
            <td>mobileAccountNo</td>
            <td>{dic["mobileAccountNo"]}PKR</td>
          </tr>

          <tr>
            <th scope="row">3</th>
            <td>emailAddress</td>
            <td>{dic["emailAddress"]}PKR</td>
          </tr>


        </tbody>
      </table>
      
      <a class="btn btn-success" href="{home}">Check Out</a>
    </div>
  </div>      
"""
class CardsWithButtonForSlider:
    def __init__(self, clas_nam,img_url, title, detail, button_url,rank ,button_tool_tip, button_name):
        self.html = f"""
<div class="card {clas_nam}" style="width: 18rem; margin-left: 10px; flex-grow:0; flex-shrink:0;">
  <img src="{img_url}" class="card-img-top" style="height: 120px;" alt="...">
  <div class="card-body">
    <p class="card-title" style="font-weight:bold">{title}</p>
    <p class="card-text" style="height: 100px; overflow: hidden;">{detail}</p>
    <p class="card-text" style="text-align: center;"> {rank}</p>
    <a href="{button_url}" class="btn btn-light border border-dark" data-bs-toggle="tooltip" data-bs-placement="bottom" title="{button_tool_tip}">{button_name}</a>
  </div>
</div>
         """
class TextBodyCardForSlider:
  def __init__(self,counter,body):
    funcfor = f"forword('_{counter}')"
    funcbac = f"backword('_{counter}')"
    self.html = f"""
    <div style="height: 10%; color:white; display:flex; justify-contant:space-between; overflow: hidden;" class="bg-dark;">
        <div class="card-body">
          {body}
        </div>
        <div style="height: 10%; display:flex; flex-direction:row">
        <button class="btn btn-light border border-dark" style = "margin-right:4px;" onclick = {funcfor}> << </button>
        <button class="btn btn-light border border-dark" onclick = {funcbac}> >> </button>
        </div>
    </div>
     """

class brand_sliders:
  def __init__(self,sector,objlis,counter,rating):
    st = ""
    for obj in objlis:
      stars = ""
      if rating > 0:
        rank = int(obj.total_rating/rating)*5
        black_stars = int(rank*5)
        # print(black_stars,rank,obj.total_rating)
        stars = ""
        for i in range(5):
          if black_stars >= 0:
            stars += "&#9733;"
            black_stars -= 1
          else:
            stars += "&#9734;"        

      st += CardsWithButtonForSlider(f"items_{counter}",f"/media/{obj.logo}",obj.name,obj.description,f"/brands/detail/{obj.pk}",stars," more information ","show details").html

    self.html = f"""
    {TextBodyCardForSlider(counter,sector).html}
    <div class = "slider_{counter} slider  bg-dark">
    {st}
    </div>    
    """
class EnterCashBar:
  def __init__(self,cashin_url,cashout_url,complete_trans_url):
    self.html = f"""
       <div class="card">
          <div class="card-body bg-dark" style="height: 10%; width: 99vw; overflow: hidden;">
            <a class = "btn btn-light m-1" href="{cashin_url}"> + Income From Inventment </a>
            <a class = "btn btn-light m-1" href="{cashout_url}"> + Investment </a>
            <a class = "btn btn-light m-1" href="{complete_trans_url}"> Complete Transaction </a>
          </div>
        </div> 
    """

class LedgerDetail:
  def __init__(self,cashin,cashout):
    item_in = "" 
    total_cashin = 0
    for cain in cashin:
      item_in += f"""    
    <tr>
      <th scope="col">{cain.date}</th>
      <th scope="col">{cain.description}</th>
      <th scope="col">{cain.amount}</th>
    </tr>"""
      total_cashin += cain.amount
    if len(cashin) < len(cashout):
      for _ in range(len(cashout) - len(cashin)):
        item_in += f"""    
    <tr>
      <th scope="col"> - </th>
      <th scope="col"> - </th>
      <th scope="col"> - </th>
    </tr>"""
    item_in += f"""
    <tr>
      <th scope="col"> - </th>
      <th scope="col">total Income</th>
      <th scope="col">{total_cashin}</th>
    </tr>"""

    cash_in_table = f"""
      <table class="table" style="color:white;width:48vw;">
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">description</th>
            <th scope="col">Income</th>
          </tr>
        </thead>
        <tbody>
              {item_in}
        </tbody>
      </table>    
    """
    item_out = "" 
    total_cashout = 0
    for cain in cashout:
      item_out += f"""    
    <tr>
      <th scope="col">{cain.date}</th>
      <th scope="col">{cain.description}</th>
      <th scope="col">{cain.amount}</th>
    </tr>"""
      total_cashout += cain.amount
    if len(cashout) < len(cashin):
      for _ in range(len(cashin) - len(cashout)):
        item_out += f"""    
    <tr>
      <th scope="col"> - </th>
      <th scope="col"> - </th>
      <th scope="col"> - </th>
    </tr>"""
    item_out += f"""
    <tr>
      <th scope="col"> - </th>
      <th scope="col">total Investment</th>
      <th scope="col">{total_cashout}</th>
    </tr>"""
    cash_out_table = f"""
      <table class="table" style="color:white;width:48vw;">
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">description</th>
            <th scope="col">Investment</th>
          </tr>
        </thead>
        <tbody>
              {item_out}
        </tbody>
      </table>    
    """
    self.html = f"""
  <div class = "bg-dark" style = "display:flex; flex-direction:row;flex-wrap:wrap;align-items: flex-start;">
    {cash_in_table}
    {cash_out_table}
  </div>
    """
class LedgerAddButton:
  def __init__(self,start_new_url):
      self.html = f"""
        <div class="card">
            <div class="card-body bg-dark" style="height: 10%; width: 99vw; overflow: hidden;">
              <a class = "btn btn-light" href="{start_new_url}"> Start new Investment </a>
            </div>
          </div>
        """

class IncomeLedger:
  def __init__(self,obj,detail_url,remove_url,totalcashin,totalcashout):
      if obj.activate:
        ending_date = "not completed"
        total_gain = totalcashin - totalcashout
        if obj.ending_date:
          ending_date = obj.ending_date
        if obj.total_gain:
          total_gain = obj.total_gain
        self.html = f"""
      <div class="card text-black bg-light m-1" style="width: 18rem;text-align:center;display:flex;flex-direction:row;flex-wrap:wrap;">
          <div class="card-header"><small style = "font-size:10px;">From {obj.starting_date} To {ending_date}</small></div>
          <div class="card-body">
          <p class="card-text">total Income {totalcashin}</p>
          <p class="card-text">total Investment {totalcashout}</p>
          <p class="card-text">profit {total_gain}</p>
          <a class="btn btn-success m-1" href="{detail_url}">details</a>
          <a class="btn btn-danger m-1" href="{remove_url}">remove</a>
        </div>
      </div>
        """
class FlexBox:
  def __init__(self,ht):
    self.html = f"""
    <div class = "bg-dark" style = "display:flex;flex-direction:row;flex-wrap:wrap;" >
    {ht}
    </div>
    """
    
class PortfolioBar:
  def __init__(self,objlis,insert_url = None,remove_url = None):
    insert = ""
    cards = ""
    ids = 0
    if objlis:
      for obj in objlis:
        cards += self.get_portfolio_card(obj,remove_url,ids)
    if insert_url:
      insert = f"""
       <div class="card">
          <div class="card-body bg-dark" style="height: 10%; width: 99vw; overflow: hidden;">
            <a class = "btn btn-light" href="{insert_url}"> Add </a>
          </div>
        </div>
      """
    self.html = f"""
    {insert}
    {TextBodyCardForSlider(ids,"Portfolio").html}
     <div class = "slider_{ids} slider  bg-dark" style = "display:flex;flex-direction:row;overflow:hidden">
        {cards}
    </div>
    """
  def get_portfolio_card(self,objlis,remove_url,ids):
    print(objlis)
    buttons = ""
    if remove_url:
      buttons += f'<a class="btn btn-success m-1" href="{objlis.project_url_link}">details</a>'
      buttons += f'<a class="btn btn-danger m-1" href="{remove_url}{objlis.pk}">remove</a>'
    else:
      buttons += f'<a class="btn btn-success" href="{objlis.project_url_link}">details</a>'
    return f""" 
    <div class="items_{ids} card text-black bg-light m-1" style="width: 18rem;text-align: center;flex-grow:0; flex-shrink:0;">
        <div class="card-header">{objlis.project_name}</div>
        <div class="card-body">
        <p class="card-text">{objlis.project_short_description}</p>
        <p class="card-text"><small>{objlis.starting_date} to {objlis.ending_date}</small></p>
        {buttons}
      </div>
    </div>
    """
