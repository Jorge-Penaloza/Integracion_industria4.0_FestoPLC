
                    final = time.time()
                    print("final",final)
                    if inicio is not  None:
                        print("tiempo_:",final - inicio)
                        if final - inicio > 5:
                            var2 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor0")
                            dv2 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                            try:
                                var2.set_value(dv2)
                            except:
                                print("An exception occurred")
                            #inicio = final
                        if final - inicio > 7:
                            var2 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor0")
                            dv2 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                            try:
                                var2.set_value(dv2)
                            except:
                                print("An exception occurred")
                            inicio = time.time()
                            print("inicio 7",inicio)
                            contador_s0 = 0
                            print("contador_s0",contador_s0)
                            exit()