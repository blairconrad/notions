rm -f order.png
create_yuml_class_diagram.py "[Customer]+1->*[Order], [Order]++1-items>*[LineItem], [Order]-0..1>[PaymentMethod]" yuml_order_example.png
