async function get_one_trip_json( trip_id ){
    fetch(`http://localhost:5000/trip/${trip_id}/json`)
        .then( response => response.json() )
        .then( results => parse_json_for_one_trip(results) )
}
get_one_trip_json(trip_id)

async function parse_json_for_one_trip (results)  {
    // console.log(results)
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
    render_for_one_trip(this_trip)
}

const render_for_one_trip = (this_trip) => {
    let lists_table = document.getElementById('lists_table')
    let output = ``
    for(let each_list in this_trip.lists ) {
        let this_list = this_trip.lists[each_list]
        if (this_list.name != null) {
            output += `
                <tr>
                    <td class="">
                        <a href="/trip/${this_trip.id}/list/${this_list.id}" 
                            class="text-decoration-none text-primary fs-5 fw-bold">
                            ${this_list.name}
                        </a>
                    </td>
                    <td class="text-end">
                    <div class="d-flex gap-2 justify-content-end">
                        <form action="/add_item" method="post">
                            <input type="hidden" name="trip_id" value=" ${this_trip.id}">
                            <input type="hidden" name="list_id" value=" ${this_list.id}">
                            <input type="hidden" name="list_name" value=" ${this_list.name}">
                            <input type="hidden" name="from_list_button" value="True">
                            <button type="submit" class="btn btn-outline-success py-0 px-2">Add Item</button>
                        </form>
                    </div>
                </tr>
            `
        for(let each_item in this_list.items) {
            let this_item = this_list.items[each_item]
            output += `
                <tr>
                    <td class="ps-4">
                        ${ this_item.name != null ? this_item.name : '<span class="text-secondary">List empty</span>'}
                    </td>
                </tr>
                `
            }
        }
        else {
            output += `
                <tr>
                    <td class="">
                        <p class="mb-1">
                            No Lists Yet
                        </p>
                    </td>
                </tr>
            `
        }
    }
    lists_table.innerHTML = output
}