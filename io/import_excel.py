def import_excel(
    session: Session,
    excel_path,
    source: str,
):
    mapping = load_mapping()
    df = pd.read_excel(excel_path)

    preview_rows = []

    for _, row in df.iterrows():
        incoming_data = {}

        for col, cfg in mapping["columns"].items():
            raw_value = row.get(col)
            value = transform_value(raw_value, cfg.get("transform"))
            incoming_data[cfg["field"]] = value

        # For UI preview
        preview_rows.append(incoming_data.copy())

        vehicles = session.query(Vehicle).all()
        matched_vehicle = None

        for vehicle in vehicles:
            if match_vehicle(
                vehicle,
                incoming_data.get("reservation_number"),
                incoming_data.get("vin"),
            ):
                matched_vehicle = vehicle
                break

        if matched_vehicle:
            sync_vehicle(
                matched_vehicle,
                incoming_data,
                source=source,
            )
        else:
            new_vehicle = Vehicle(**incoming_data)
            new_vehicle.source_file = source
            session.add(new_vehicle)

    session.commit()
    return preview_rows
