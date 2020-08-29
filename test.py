import cbapi

def test_cbapi():
  try:
    cbapi.set_rapidapi_key('e4278c7177msh6cfd99955256eccp1a4ed0jsn2953832534cb')
    df_ppl = cbapi.get_people(name='Steve',types='investor', parallel=True)
    df_org = cbapi.get_organizations(name='Data', parallel=True)
  except Exception:
    print("Execution Error")

if __name__ == "__main__":
    test_cbapi()



