def switch_page(system_state, page_name):
    system_state["pages"][page_name].tkraise()