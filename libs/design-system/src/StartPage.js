import React from 'react';
import { Main } from '@digigov/ui/layouts/Basic';
import Paragraph from '@digigov/ui/typography/Paragraph';
import PageTitle, { PageTitleHeading } from '@digigov/ui/app/PageTitle';
import CallToActionButton from '@digigov/ui/core/Button/CallToAction';
import Layout from "@diplomas/design-system/Layout";


export default function StartPage(props) {
    return (
        <Layout>
            <Main >
                <PageTitle>
                    <PageTitleHeading>{props.title}</PageTitleHeading>
                </PageTitle>
                <Paragraph>{props.text}</Paragraph>
                <CallToActionButton href={props.href}>Enter here</CallToActionButton>
            </Main>
        </Layout>
    );
}