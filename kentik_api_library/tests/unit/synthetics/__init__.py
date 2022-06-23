import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb


def protobuf_assert_equal(a, b, path: str) -> None:
    """Compare two protobuf structures - the actual stored values, not references"""

    fields = sorted((f.name for f, _ in a.ListFields() + b.ListFields()))
    for name in fields:
        ac = getattr(a, name)
        bc = getattr(b, name)
        if hasattr(ac, "ListFields"):
            protobuf_assert_equal(ac, bc, path + "." + name)
        else:
            assert ac == bc, f"{path}.{name}: '{ac}' != '{bc}'"


def clear_readonly_fields(test: pb.Test) -> pb.Test:
    """For sending a request - clear the server-generated fields"""

    test.ClearField("cdate")
    test.ClearField("created_by")
    test.ClearField("last_updated_by")
    return test
