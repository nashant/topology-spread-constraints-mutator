from OpenSSL.crypto import load_certificate, FILETYPE_PEM, X509Store, X509StoreContext, X509StoreContextError


def verify_chain():
    with open("/app/certs/ca.crt") as f:
        root_cert = load_certificate(FILETYPE_PEM, f.read())

    with open("/app/certs/tls.crt") as f:
        tls_cert = load_certificate(FILETYPE_PEM, f.read())

    store = X509Store()
    store.add_cert(root_cert)

    store_ctx = X509StoreContext(store, tls_cert)
    try:
        store_ctx.verify_certificate()
        return True
    except X509StoreContextError:
        return False