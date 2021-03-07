USE [TimeEntryDB]
GO

/****** Object:  Table [dbo].[DimClientEngagements]    Script Date: 3/7/2021 2:57:41 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimClientEngagements](
	[ClientID] [nchar](10) NOT NULL,
	[ClientName] [varchar](max) NULL,
	[EngagementID] [nchar](10) NOT NULL,
	[EngagementName] [varchar](max) NULL,
	[Region] [varchar](50) NULL,
	[EngagementStatus] [varchar](50) NULL,
	[Client_Engagement]  AS (([ClientName]+' - ')+[EngagementName])
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


