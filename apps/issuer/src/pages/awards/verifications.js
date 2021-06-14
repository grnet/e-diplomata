import React from 'react';
import VerificationsTable from "@diplomas/design-system/VerificationsTable";

export default function Verifications() {
    const data = [{ id: '0', type: 'Grnet', status: 'Success' }]
    return (
        <>
            <VerificationsTable
                data={data}
            />
        </>
    )
}