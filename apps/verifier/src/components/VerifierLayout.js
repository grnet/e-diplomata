import BasicLayout, { Bottom, Top, Content } from "@digigov/ui/layouts/Basic";
import GovGRFooter from "@digigov/ui/govgr/Footer";
import GovGRLogo from "@digigov/ui/govgr/Logo";
import Header, { HeaderTitle } from "@digigov/ui/app/Header";
import ServiceBadge from "@digigov/ui/core/ServiceBadge";

export default function VerifierLayout({ children }) {
  return (
    <BasicLayout>
      <Top>
        <Header>
          <GovGRLogo />
          <HeaderTitle>
            Service name
            <ServiceBadge label="PREALPHA" />
          </HeaderTitle>
        </Header>
      </Top>
      <Content>{children}</Content>
      <Bottom>
        <GovGRFooter />
      </Bottom>
    </BasicLayout>
  );
}
