async function get_one_trip_json( trip_id ){
    fetch(`http://localhost:5000/trip/${trip_id}/json`)
        .then( response => response.json() )
        .then( results => parse_json_for_one_trip(results) )
}
get_one_trip_json(trip_id)

async function parse_json_for_one_trip (results)  {
    let data  = results.this_trip_json
    let this_trip = {
        id : data[0].id,
        name : data[0].name,
        location : data[0].location,
        date : data[0].date,
        days : data[0].days,
        user_id : data[0].user_id,
        lists : {},
    }
    for (let each_list in data) {
        let list_data = {
            id : data[each_list]['lists.id'],
            name : data[each_list]['lists.name'],
            trip_id : data[each_list]['trip_id'],
            items : {},
        }
        let current_list_id = data[each_list]['lists.id']
        this_trip['lists'][current_list_id] = list_data
    }
    for (let each_item in data) {
        let item_data = {
            id : data[each_item]['items.id'],
            name : data[each_item]['items.name'],
            unit : data[each_item]['unit'],
            quantity : data[each_item]['quantity'],
            is_packed : data[each_item]['is_packed'],
            list_id : data[each_item]['lists.id'],
        }
        let current_list_id = data[each_item]['lists.id']
        let current_item_id = data[each_item]['items.id']
        this_trip['lists'][current_list_id].items[current_item_id] = item_data
    }
    if ( typeof item_id !== 'undefined' ){
        render_for_one_item(this_trip)
    }
    else if ( typeof list_id !== 'undefined' ){
        render_for_one_list(this_trip)
    }
    else {
        render_for_one_trip(this_trip)
    }
}

async function render_for_one_trip (this_trip) {
    let lists_table = document.getElementById('lists_table')
    let output = ``
    for(let each_list in this_trip.lists ) {
        let this_list = this_trip.lists[each_list]
        if (this_list.name != null) {
            output += `
                <tr>
                    <td class="d-flex justify-content-between">
                        <div class="d-flex gap-2 align-items-center">
                            <a href="/trip/${this_trip.id}/list/${this_list.id}" 
                                class="text-decoration-none text-primary fs-5 fw-bold">
                                ${this_list.name} 
                            </a>
                            <span class="complete fs-5 ps-2">COMPLETE!</span>
                        </div>
                        <div>
                            <form action="/add_item" method="post">
                                <input type="hidden" name="trip_id" value=" ${this_trip.id}">
                                <input type="hidden" name="list_id" value=" ${this_list.id}">
                                <input type="hidden" name="list_name" value=" ${this_list.name}">
                                <input type="hidden" name="from_list_button" value="True">
                                <button type="submit" class="btn btn-outline-success py-0 px-2">Add Item</button>
                            </form>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>
                        <table class="pony">
            `
            for(let each_item in this_list.items) {
                let this_item = this_list.items[each_item]
                if(this_item.name != null) {
                    output += `
                        <tr>
                            <td class="px-4">
                                <form action="" class="d-flex gap-3">
                                    <input type="checkbox" name="is_packed" id="is_packed_for_item_${this_item.id}" 
                                        ${this_item.is_packed ? 'checked' : ''} >
                                    <label for="is_packed_for_item_${this_item.id}">${this_item.name}</label>
                                </form>
                            </td>
                        </tr>
                    `
                }
                else {
                    output += `
                        <tr>
                            <td class="ps-4">
                                <span class="text-secondary">List empty</span>
                            </td>
                        </tr>
                    `
                }
            }
            output += `
                        </table>
                    </td>
                </tr>
            `
        }
        else {
            output += `
                <tr>
                    <td class="">
                        <p class="mb-1 text-secondary">
                            No Lists Yet
                        </p>
                    </td>
                </tr>
            `
        }
    }
    lists_table.innerHTML = output
    check_for_complete_list_by_html()
    add_listeners(this_trip)
}

async function render_for_one_list (this_trip) {
    let items_table = document.getElementById('items_table')
    items_table.parentElement.className = 'pony'
    let this_list = this_trip.lists[list_id]
    let output = ``
    for(let each_item in this_list.items) {
        let this_item = this_list.items[each_item]
        if ( this_item.name != null) {
            output += `
                <tr>
                    <td class="d-flex justify-content-between align-items-center p-2">
                        <form action="" class="" id="form_for_item_${this_item.id}">
                            <div class="">
                                <input class="form-check-input me-2" type="checkbox" name="is_packed_for_item_${this_item.id}" id="is_packed_for_item_${this_item.id}" 
                                    ${this_item.is_packed ? 'checked' : ''} placeholder="">
                                <label class="form-label mb-0" for="is_packed_for_item_${this_item.id}">
                                    ${this_item.name}
                                </label>
                            </div>
                        </form>
                        <a href="/trip/${this_trip.id}/list/${this_list.id}/item/${this_item.id}" 
                            class="btn btn-sm btn-outline-info text-decoration-none py-0 px-2">
                            Details
                        </a>
                    </td>
                </tr>
            `
        }
        else {
            output += `
                <tr>
                    <td class="">
                        <span class="text-secondary">List empty</span>
                    </td>
                </tr>
            `
        }
    }
    items_table.innerHTML = output
    check_for_complete_list_by_html()
    add_listeners(this_trip)
    return
}

async function render_for_one_item (this_trip) {
    let item_check_input = document.getElementById('item_check_input')
    let this_list = this_trip.lists[list_id]
    let this_item = this_list.items[item_id]
    let output = ``
    if ( this_item.name != null) {
        output += `
            <input class="form-check-input me-2" type="checkbox" 
                name="is_packed_for_item_${this_item.id}" id="is_packed_for_item_${this_item.id}" 
                ${this_item.is_packed ? 'checked' : ''} placeholder="">
            <label class="form-label mb-0" for="is_packed_for_item_${this_item.id}">
                Is it Packed?
            </label>
        `
    }
    item_check_input.innerHTML = output
    check_for_complete_list_by_html()
    add_listeners(this_trip)
    return
}

async function add_listeners (this_trip) {
    for( let each_list in this_trip.lists ){
        let this_list = this_trip.lists[each_list]
        if ( typeof list_id !== 'undefined' && this_list.id != list_id ){ continue; }
        for( let each_item in this_list.items ){
            let this_item = this_list.items[each_item]
            if ( typeof item_id !== 'undefined' && this_item.id != item_id ){ continue; }
            if ( this_item.name != null) {
                this_item['element'] = document.getElementById(`is_packed_for_item_${this_item.id}`)
                this_item['element'].addEventListener("change", (event) => {
                    update_checkbox(this_trip, this_item, event)
                })
            }
        }
    }
    return
}

async function update_checkbox (this_trip, this_item, event) {
    let form = new FormData()
    form.append('name', this_item.name)
    form.append('unit', this_item.unit)
    form.append('quantity', this_item.quantity)
    form.append('is_packed', event.target.checked)
    form.append('item_id', this_item.id)
    form.append('trip_id', trip_id)
    form.append('list_id', this_item.list_id)
    
    fetch(`http://localhost:5000/trip/${trip_id}/list/${this_item.list_id}/item/${this_item.id}/edit/json`, { method :'POST', body : form})
        .then( response => response.json() )
        .then( data => check_for_complete_list_by_html() )
    return
}

async function check_for_complete_list_by_html () {
    let all_list_containers = document.getElementsByClassName('pony')
    let all_completes = document.getElementsByClassName('complete')
    let total_checkbox_elements = []
    let checked_boxes_per_TRIP_count = 0
    for(let i=0 ; i< all_list_containers.length; i++){
        inputs = all_list_containers[i].getElementsByTagName('input')
        let checked_boxes_per_list_count = 0
        for(let j=0; j<inputs.length; j++){
            total_checkbox_elements.push(inputs[j])
            if (inputs[j].checked){
                checked_boxes_per_list_count++
                checked_boxes_per_TRIP_count++
            }
        }
        if( checked_boxes_per_list_count == inputs.length ) {
            if(all_list_containers[i].innerText == "List empty"){
                continue
            }
            all_list_containers[i].className = 'pony table table-hover table-sm table-striped table-success'
            all_completes[i].style.display = 'inline'
        }
        else {
            all_list_containers[i].className = 'pony table table-hover table-sm table-striped'
            all_completes[i].style.display = 'none'
        }
    }
    
    all_packed = document.getElementById('final_victory')
    if (all_packed) {
        if( total_checkbox_elements.length > 0 && checked_boxes_per_TRIP_count == total_checkbox_elements.length){
            all_packed.style.display = 'block'
        }
        else {
            all_packed.style.display = 'none'
        }
        return
    }
}