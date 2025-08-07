import { ThreeDotsLoader } from "@/components/Loading";
import { getDatesList, useZakkBotAnalytics } from "../lib";
import { DateRangePickerValue } from "@/components/dateRangeSelectors/AdminDateRangeSelector";
import Text from "@/components/ui/text";
import Title from "@/components/ui/title";
import CardSection from "@/components/admin/CardSection";
import { AreaChartDisplay } from "@/components/ui/areaChart";

export function ZakkBotChart({
  timeRange,
}: {
  timeRange: DateRangePickerValue;
}) {
  const {
    data: zakkBotAnalyticsData,
    isLoading: isZakkBotAnalyticsLoading,
    error: zakkBotAnalyticsError,
  } = useZakkBotAnalytics(timeRange);

  let chart;
  if (isZakkBotAnalyticsLoading) {
    chart = (
      <div className="h-80 flex flex-col">
        <ThreeDotsLoader />
      </div>
    );
  } else if (
    !zakkBotAnalyticsData ||
    zakkBotAnalyticsData[0] == undefined ||
    zakkBotAnalyticsError
  ) {
    chart = (
      <div className="h-80 text-red-600 text-bold flex flex-col">
        <p className="m-auto">Failed to fetch feedback data...</p>
      </div>
    );
  } else {
    const initialDate =
      timeRange.from || new Date(zakkBotAnalyticsData[0].date);
    const dateRange = getDatesList(initialDate);

    const dateToZakkBotAnalytics = new Map(
      zakkBotAnalyticsData.map((zakkBotAnalyticsEntry) => [
        zakkBotAnalyticsEntry.date,
        zakkBotAnalyticsEntry,
      ])
    );

    chart = (
      <AreaChartDisplay
        className="mt-4"
        data={dateRange.map((dateStr) => {
          const zakkBotAnalyticsForDate = dateToZakkBotAnalytics.get(dateStr);
          return {
            Day: dateStr,
            "Total Queries": zakkBotAnalyticsForDate?.total_queries || 0,
            "Automatically Resolved":
              zakkBotAnalyticsForDate?.auto_resolved || 0,
          };
        })}
        categories={["Total Queries", "Automatically Resolved"]}
        index="Day"
        colors={["indigo", "fuchsia"]}
        yAxisWidth={60}
      />
    );
  }

  return (
    <CardSection className="mt-8">
      <Title>Slack Channel</Title>
      <Text>Total Queries vs Auto Resolved</Text>
      {chart}
    </CardSection>
  );
}
