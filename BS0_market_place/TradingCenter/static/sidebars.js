/* global bootstrap: false */
objects = {}
function determine(ids){

}
function forword(ids) {
    console.log("ids is" , ids)
    if (objects["slider"+ids] == undefined){
        objects["slider"+ids] = {"mouseX":0,"currentElement":0}
      }

    objects['slider'+ids].currentElement += 1
    makeslider(ids)

}
function backword(ids) {
    if (objects["slider"+ids] == undefined){
        objects["slider"+ids] = {"mouseX":0,"currentElement":0}
      }
    objects['slider'+ids].currentElement -= 1
    makeslider(ids)
 }
function rotation(n, itemslen) {
    index = []
    for(i=0;i<itemslen;i++){
        if (n >= itemslen) {
            n = 0;
        }
        index.push(n);
        n = n + 1;
    }
    return index;
}
function makeslider(ids){
    elements = document.getElementsByClassName("items"+ids)
    size = elements.length
    if(objects['slider'+ids].currentElement >= size){ objects['slider'+ids].currentElement = 0 }
    if(objects['slider'+ids].currentElement < 0){objects['slider'+ids].currentElement = size}
    Indexes = rotation(objects['slider'+ids].currentElement,size)
    for(i=0;i<size;i++){
        elements[i].style.order = Indexes[i]
    }
}