async function get_one_list_json( trip_id, list_id ){
    fetch(`http://localhost:5000/trip/${trip_id}/json`)
        .then( response => response.json() )
        .then( results => parse_json_for_one_list(results) )
}
get_one_list_json(trip_id, list_id);

async function parse_json_for_one_list (results)  {
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
        }
        let current_list_id = data[each_item]['lists.id']
        let current_item_id = data[each_item]['items.id']
        this_trip['lists'][current_list_id].items[current_item_id] = item_data
    }
    render_for_one_list(this_trip)
}

const render_for_one_list = (this_trip) => {
    let items_table = document.getElementById('items_table')
    let this_list = this_trip.lists[list_id]
    let output = ``

    for(let each_item in this_list.items) {
        let this_item = this_list.items[each_item]
        if ( this_item.name != null) {
            output += `
                <tr>
                    <td class="">
                        <a href="/trip/${this_trip.id}/list/${this_list.id}/item/${this_item.id}" 
                            class="text-decoration-none text-primary fs-5 fw-bold">
                            ${this_item.name}
                        </a>
                    </td>
                    <td class="text-end">
                        <form action="" id="form_for_item_${this_item.id}">
                            <div class="">
                                <input class="form-check-input me-2" type="checkbox" name="is_packed" id="is_packed_for_item_${this_item.id}" 
                                    ${this_item.is_packed ? 'checked' : ''} placeholder="">
                                <label class="form-label mb-0" for="is_packed"></label>
                            </div>
                        </form>
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
    add_listeners(this_list)
}

async function add_listeners (this_list) {
    for(let each_item in this_list.items) {
        let this_item = this_list.items[each_item]
        if ( this_item.name != null) {
            this_item['element'] = document.getElementById(`is_packed_for_item_${this_item.id}`)
            this_item['element'].addEventListener("change", (event) => {
                update_checkbox(this_item, event)
            })
        }
    }
}

async function update_checkbox (this_item, event) {
    let form = new FormData()
    form.append('name', this_item.name)
    form.append('unit', this_item.unit)
    form.append('quantity', this_item.quantity)
    form.append('is_packed', event.target.checked)
    form.append('item_id', this_item.id)
    form.append('trip_id', trip_id)
    form.append('list_id', list_id)

    fetch(`http://localhost:5000/trip/${trip_id}/list/${list_id}/item/${this_item.id}/edit/json`, { method :'POST', body : form})
        .then( response => response.json() )
        .then( data => console.log(data) )
}