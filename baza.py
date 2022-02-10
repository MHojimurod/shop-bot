a = ["start", "request_name", "request_number", "send_number", "select_region", "select_district", "district_not_found", "region_not_found", "language_not_found", "order_accepted", "order_delivered", "order_denied", "accept_message", "reject_message",
    "i_bought", "prompt_end", "promotion_count_message", "promotion_count_error", "empty_busket", "pay_type", "cash", "loan", "no_orders", "are_you_sure_get_gift", "yes", "no", "not_enought_balls", "accept_your_prompt", "not_access", "taken", "buy", "my_balls","send_cvitation","send_cvi_serial_number","cvitation_success","already_sold","seria_not_found","shop_name","add_to_cart","order_btn","add_again_btn","back_btn","balls"]


from admin_panel.models import Text



for i in a:
    Text.objects.create(name=i,uz_data=i,ru_data=i)